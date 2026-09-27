import json
import unittest
from contract_harness import Harness, UserError, Address, Return

class DedupTests(unittest.TestCase):
    def setUp(self):
        self.h=Harness('grant-dedup','GrantDedup');self.c=self.h.contract
        self.c.enroll(Address('a'),'Build an open-source wallet for local merchants.')
        self.c.enroll(Address('b'),'Build an open-source wallet for local merchants with a new name.')

    def test_full_prefix_and_duplicate(self):
        self.c.review(0)
        pair={'relation':'DUPLICATE','candidate_quote':'wallet for local merchants','prior_quote':'wallet for local merchants'}
        self.h.respond({'pairs':[pair]});self.c.review(1)
        self.assertEqual(json.loads(self.c.get_review(1))['outcome'],'DUPLICATE')
        with self.assertRaises(UserError):self.c.review(1)

    def test_validator_cannot_skip_a_prior_entry(self):
        self.h.outputs=[{'pairs':[]}]
        with self.assertRaises(UserError):self.c.review(1)

    def test_independent_substantive_disagreement(self):
        def output(r):return {'pairs':[{'relation':r,'candidate_quote':'wallet for local merchants','prior_quote':'wallet for local merchants'}]}
        self.h.respond(output('DISTINCT'),output('DUPLICATE'))
        with self.assertRaisesRegex(UserError,'consensus rejected'):self.c.review(1)
        self.assertEqual(len(self.c.reviews),0)

    def test_curator_access_and_capacity(self):
        self.h.gl.message.sender_address=Address('outsider')
        with self.assertRaises(UserError):self.c.enroll(Address('x'),'spam proposal')
        self.h.gl.message.sender_address=Address('sponsor')
        for i in range(14):self.c.enroll(Address('x'),f'proposal {i}')
        with self.assertRaises(UserError):self.c.enroll(Address('x'),'overflow proposal')

if __name__ == '__main__': unittest.main()
