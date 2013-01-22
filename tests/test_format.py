#!/usr/bin/env python
from __future__ import division

__author__ = "Jai Ram Rideout"
__copyright__ = "Copyright 2013, The QIIME Project"
__credits__ = ["Jai Ram Rideout"]
__license__ = "GPL"
__version__ = "0.0.0-dev"
__maintainer__ = "Jai Ram Rideout"
__email__ = "jai.rideout@gmail.com"

"""Test suite for the format.py module."""

from unittest import main, TestCase

from my_microbes.format import format_participant_table, create_alpha_diversity_boxplots_html

class FormatTests(TestCase):
    """Tests for the format.py module."""

    def setUp(self):
        """Define some sample data that will be used by the tests."""
        # Standard recipients file with two recipients, one with multiple email
        # addresses.
        self.recipients = ["# a comment", " ", " foo1\tfoo@bar.baz  ",
                           "foo2\t foo2@bar.baz,  foo3@bar.baz,foo4@bar.baz "]

        # An empty recipients file.
        self.empty_recipients = ["# a comment", " ", "\n\t\t\t\t"]

    def test_format_participant_table(self):
        """Test formatting an HTML table of study participants."""
        # Test URL prefix without trailing slash.
        exp = ('<table class="data-table">\n'
               '<tr><th>Personal ID</th></tr>\n'
               '<tr><td><a href="http://my-microbes.qiime.org/'
                 'foo1/index.html">foo1</a></td></tr>\n'
               '<tr><td><a href="http://my-microbes.qiime.org/'
                 'foo2/index.html">foo2</a></td></tr>\n'
               '</table>\n')
        obs = format_participant_table(self.recipients,
                                       'http://my-microbes.qiime.org')
        self.assertEqual(obs, exp)

        # Test URL prefix with trailing slash.
        obs = format_participant_table(self.recipients,
                                       'http://my-microbes.qiime.org/')
        self.assertEqual(obs, exp)

        # Test empty recipients file.
        exp = ('<table class="data-table">\n'
               '<tr><th>Personal ID</th></tr>\n'
               '</table>\n')
        obs = format_participant_table(self.empty_recipients,
                                       'http://my-microbes.qiime.org')
        self.assertEqual(obs, exp)
        
    def test_create_alpha_diversity_boxplots_html(self): 
        """Test alpha diversity boxplots"""
        input = ('pd.txt', 'chao.txt')
        exp = expected_alpha_diversity_boxplots
        self.assertEqual(create_alpha_diversity_boxplots_html(input), exp)


expected_alpha_diversity_boxplots = """
<h2>Alpha Diversity Boxplots</h2>
Here we present a series of comparative boxplots showing the
distributions of your alpha diversity (<i>Self</i>) versus all other
individuals' alpha diversity (<i>Other</i>) for each body site.
Separate boxplots are provided for each alpha diversity metric. For
more details about alpha diversity, please refer to the
<b>Alpha Rarefaction</b> tab.

<h3>Click on the following links to see your alpha diversity boxplots:</h3>
<ul>
  <li><a href="pd.txt">pd</a></li><li><a href="chao.txt">chao</a></li>
</ul>
"""

if __name__ == "__main__":
    main()
