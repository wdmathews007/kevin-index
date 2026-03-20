import unittest

from grammer_rules.punctuationRules import parenthesesFreq, semicolonFreq
from grammer_rules.scentenceStarters import (
    sentences_starter_and,
    sentences_starter_but,
    sentences_starter_discourse,
    sentences_starter_the,
)
from grammer_rules.sentenceStructure import (
    sentences_structure_avg,
    sentences_structure_std_dev,
)
from grammer_rules.structuralDiscourse import avg_para_length, std_dev_para_length
from grammer_rules.wordChoice import (
    avg_word_length,
    contraction_rate,
    discourse_marker_rate,
    filler_word_rate,
    type_token_ratio,
)


class GrammarRulesTest(unittest.TestCase):
    def test_empty_text_returns_zero_for_core_rates(self):
        self.assertEqual(semicolonFreq(""), 0)
        self.assertEqual(sentences_starter_but(""), 0)
        self.assertEqual(contraction_rate(""), 0)
        self.assertEqual(type_token_ratio(""), 0)
        self.assertEqual(avg_word_length(""), 0)

    def test_sentence_starters_handle_end_of_string_and_multiword_starter(self):
        self.assertEqual(sentences_starter_and("And we left"), 100)
        self.assertEqual(sentences_starter_the("The cat sat"), 100)
        self.assertEqual(
            sentences_starter_discourse("In conclusion, this works"),
            100,
        )

    def test_word_choice_normalizes_punctuation_and_case(self):
        self.assertEqual(contraction_rate("It's, fine."), 50)
        self.assertEqual(filler_word_rate("Really, very good."), 200 / 3)
        self.assertEqual(type_token_ratio("Word word, WORD"), 1 / 3)
        self.assertEqual(avg_word_length("Hi, there."), 3.5)

    def test_discourse_marker_rate_counts_multiword_phrases(self):
        self.assertEqual(
            discourse_marker_rate("In conclusion, this works."),
            25,
        )

    def test_sentence_and_paragraph_metrics_use_sentence_counts(self):
        text = "One two. Three.\n\nFour."
        self.assertEqual(sentences_structure_avg(text), 4 / 3)
        self.assertAlmostEqual(sentences_structure_std_dev(text), 0.4714045207910317)
        self.assertEqual(avg_para_length(text), 1.5)
        self.assertEqual(std_dev_para_length(text), 0.5)

    def test_parentheses_frequency_counts_both_sides(self):
        self.assertEqual(parenthesesFreq("(one)"), 2)


if __name__ == "__main__":
    unittest.main()
