# -*- coding: utf-8 -*-
from docutils.nodes import section
from docutils.parsers.rst import Directive
from docutils.statemachine import ViewList
import pkg_resources


class IncludeChangelog(Directive):
    """
    """
    required_arguments = 1
    has_content = False

    def __init__(self,
                 directive,
                 arguments,
                 options,           # ignored
                 content,           # ignored
                 lineno,            # ignored
                 content_offset,    # ignored
                 block_text,        # ignored
                 state,
                 state_machine,     # ignored
                ):
        assert directive == 'includechangelog'
        assert len(arguments) == 1
        self.module = arguments[0]
        self.state = state
        self.lineno = lineno

    def run(self):
        doc = ViewList()
        packageInfos = pkg_resources.WorkingSet().find(pkg_resources.Requirement.parse(self.module))._get_metadata('PKG-INFO')
        addLine = False
        doc.append(u'', '<includedoc>')
        for line in packageInfos:
            if 'Platform: ' in line:
                break
            if addLine or line in ['Changes', 'Changelog']:
                addLine = True
                doc.append(line.decode('utf-8'), '<includedoc>')
        doc.append(u'', '<includedoc>')
        node = section()
        surrounding_title_styles = self.state.memo.title_styles
        surrounding_section_level = self.state.memo.section_level
        self.state.memo.title_styles = []
        self.state.memo.section_level = 0
        self.state.nested_parse(doc, 0, node, match_titles=1)
        self.state.memo.title_styles = surrounding_title_styles
        self.state.memo.section_level = surrounding_section_level
        return node.children


def setup(app):
    app.add_directive('includechangelog', IncludeChangelog)
