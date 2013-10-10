import os.path
from glob import glob
from itertools import chain
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from django.db import transaction

from readfast.models import Piece
from readfast.parser import PieceParser


def get_or_else(dact, name, default):
    return getattr(dact, name, default)

def get_or_space(dact, name):
    return get_or_else(dact, name, ' ')

def get_or_thousand(dact, name):
    return get_or_else(dact, name, 1000)

class Command(BaseCommand):
    args = "<dir_or_file ...>"
    help = "Import corpora from files or directories."

    option_list = BaseCommand.option_list + (
        make_option("-n", "--dry-run",
                    action="store_true",
                    dest="dry_run",
                    default=False,
                    help="Don't actually create the models"),
    )

    def handle(self, *args, **kwargs):
        if not args:
            raise CommandError("No files or directories provided")

        stripped_names = [arg.rstrip("/") for arg in args]
        missing = [n for n in stripped_names if not os.path.exists(n)]
        if missing:
            raise CommandError("Missing: %s" % ", ".join(missing))

        file_lists = map(self._filenames, stripped_names)
        # Schlomp all the lists together
        files_to_import = list(chain(*file_lists))

        for corpus_filename in files_to_import:
            print "Processing %s" % os.path.basename(corpus_filename)
            with open(corpus_filename) as corpus_file:
                parser = PieceParser(corpus_file)
                if kwargs["dry_run"]:
                    print "Not saving"
                else:
                    with transaction.commit_on_success():
                        piece = Piece(name=get_or_space(parser,'title'),
                                       slug=slugify(get_or_space(parser,'title')),
                                       text=get_or_space(parser,'text'),
                                       order=get_or_thousand(parser, 'order'),
                                       source_url=get_or_space(parser,'url'),
                                       source_title=get_or_space(parser,'source'),
                                       author=get_or_space(parser,'author'))
                        piece.save()
                        for parsed_question in parser.questions:
                            question_model = piece.questions.create(
                                text=parsed_question.text
                            )
                            for parsed_answer in parsed_question.answers:
                                question_model.answers.create(
                                    text=parsed_answer.text,
                                    correct=parsed_answer.correct
                                )

    def _filenames(self, dir_or_file):
        """All filenames from a file or directory path."""
        if os.path.isdir(dir_or_file):
            return glob(os.path.join(dir_or_file, "*.txt"))
        else:
            return [dir_or_file]
