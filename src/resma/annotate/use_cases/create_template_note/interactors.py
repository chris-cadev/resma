from datetime import datetime, timedelta
from dateutil.parser import parse as dateutil_parse
import re
from typing import Optional
from resma.annotate.interfaces.interactors import AnnotateTemplateNoteInteractor, AnnotateTemplateRepositoryInteractor
from resma.annotate.use_cases.note.interactors import NoteInteractor
from os.path import join
from resma.annotate.interfaces.dto import NoteDTO, NoteWithContentDTO, TemplateDTO


class CreateTemplateNoteInteractor(NoteInteractor):
    def __init__(
        self,
        *,
        notes_repo,
        config,
        templates_repo: AnnotateTemplateRepositoryInteractor,
        note_template_interactor: AnnotateTemplateNoteInteractor,
    ):
        super().__init__(notes_repo=notes_repo, config=config)
        self.templates_repo = templates_repo
        self.note_template_interactor = note_template_interactor

    def execute(self, *, name: Optional[str] = None, vault: Optional[str] = None, template: Optional[str] = None, meta: Optional[dict]) -> NoteDTO:
        note_path = self.get_note_filepath(name=name, vault=vault)
        template_path = self.get_template_filepath(
            vault=vault, template=template
        )
        if template_path:
            template_filepath = join(self.config.templates_dir, template_path)
        try:
            note = self.notes_repo.get(filepath=note_path)
        except ValueError:
            note = self.notes_repo.create(filepath=note_path)
        template_selected = self.templates_repo.get(
            filepath=template_filepath)
        template_evaluated = self.note_template_interactor.evaluate_template(
            template=template_selected,
            note=note,
            meta=meta,
        )

        note = self.notes_repo.append(
            filepath=note.filepath, content=template_evaluated.content)

        return note

    def get_template_filepath(self, *, vault: str, template: Optional[str] = None) -> str:
        vault_templates = self.config.templates['vault'].get(vault, {})
        template_filepath = vault_templates.get(template)

        if template_filepath is None:
            template_filepath = self.config.templates.get(template)

        if template_filepath is None:
            raise KeyError(
                f"Template '{template}' not found in vault '{vault}' or global templates.")

        return template_filepath


class TimelineNoteInteractor(AnnotateTemplateNoteInteractor):
    DATE_FORMAT = '%A %d-%b-%Y'

    def evaluate_template(self, *, template: TemplateDTO, note: Optional[NoteWithContentDTO] = None, meta: Optional[dict] = {}) -> NoteWithContentDTO:
        date = meta.get('date')
        entry_date = dateutil_parse(
            date) if date is not None else datetime.today()
        prev_entry_date = self.get_latest_date_entry(note)
        diff_days = (entry_date - prev_entry_date).days
        if prev_entry_date and diff_days < 1:
            raise ValueError("Date between entries must be at least one day apart.")
        prev_day_name = self.get_prev_day_name(prev_entry_date, entry_date)
        replacements = {
            "date:: ==date==": None if not entry_date else f'date:: {entry_date.strftime(TimelineNoteInteractor.DATE_FORMAT)}',
            "**==prev-day-name==**": None if not prev_day_name else f'**{prev_day_name}**',
            "==prev-entry-date==":  None if not prev_entry_date else prev_entry_date.strftime(TimelineNoteInteractor.DATE_FORMAT),
        }
        for placeholder, value in replacements.items():
            if not value:
                template.content = template.content.replace(placeholder, '')
                continue
            template.content = template.content.replace(placeholder, value)
        return NoteWithContentDTO(
            filepath=note.filepath,
            content=template.content,
        )

    def get_latest_date_entry(self, note: NoteWithContentDTO):
        dates = self.get_date_matches(note.content)
        if not dates:
            return None
        latest_date = dates[0]
        date = latest_date.split("::")[1].strip()
        return dateutil_parse(date) if date else None

    def get_date_matches(self, content: str):
        pattern = r'date::\s*\w+\s\d{2}-[A-Za-z]{3}-\d{4}'
        matches = re.findall(pattern, content, re.IGNORECASE)
        return list(reversed(matches))

    def get_prev_day_name(self, previous_date: Optional[datetime] = None, next_date: Optional[datetime] = None):
        if not previous_date:
            return None
        days_away = (next_date - previous_date).days
        if days_away == 0:
            return 'today'
        if days_away == 1:
            return 'yesterday'
        return f'on {self.get_day_name(previous_date)}'

    def get_day_name(self, date_string: str):
        days = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday']
        date = datetime.strptime(
            date_string, TimelineNoteInteractor.DATE_FORMAT)
        day_of_week = date.weekday()
        return days[day_of_week]
