"""Offline regression tests for complete, bounded HF inventory checks.

Run: python3 -m unittest discover -s scripts -p test_atlas_release_watch.py
"""
import json
import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import check_base_model_releases as watch


class InventoryTests(unittest.TestCase):
    def inspect(self, responses):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            output=root/'out'; output.mkdir()
            previous=root/'previous'; previous.mkdir()
            with patch.object(watch,'fetch_response',side_effect=responses):
                result=watch.fetch_job(('org','https://huggingface.co/api/models?author=org','.json','inventory','team'),output,previous,'2026-09-16')
            return result, list(output.iterdir())

    def test_pagination_keeps_historical_ids_without_calling_them_recent(self):
        result,_=self.inspect([
            (json.dumps([{'id':'org/new','createdAt':'2026-10-01'}]).encode(),'application/json','<https://huggingface.co/api/models?cursor=two>; rel="next"'),
            (json.dumps([{'id':'org/old','createdAt':'2025-01-01'}]).encode(),'application/json',''),
        ])
        self.assertEqual(result['itemCount'],2)
        self.assertTrue(result['paginationComplete'])
        self.assertEqual(result['recentCandidates'],['org/new'])
        self.assertIn('org/old',result['newRepositories'])

    def test_pagination_loop_does_not_save_partial_success(self):
        result,files=self.inspect([(b'[]','application/json','<https://huggingface.co/api/models?author=org>; rel="next"')])
        self.assertEqual(result['status'],'failed')
        self.assertEqual(files,[])

    def test_existing_repository_edit_is_a_review_signal_not_a_new_model(self):
        result, _ = self.inspect([(json.dumps([
            {'id': 'org/historical', 'createdAt': '2025-01-01',
             'lastModified': '2026-10-31T01:00:00Z'},
        ]).encode(), 'application/json', '')])
        self.assertEqual(result['recentCandidates'], [])
        self.assertEqual(result['modifiedCandidates'], ['org/historical'])
        self.assertEqual(result['changedRepositories'], [])
        self.assertTrue(result['modificationTrackingBaseline'])
        self.assertIn('not new releases', result['comparisonNote'])

    def test_external_pagination_is_rejected(self):
        result,files=self.inspect([(b'[]','application/json','<https://example.com/api/models>; rel="next"')])
        self.assertEqual(result['status'],'failed')
        self.assertEqual(files,[])

    def test_curl_is_bounded_beyond_socket_timeout(self):
        with patch.object(watch.subprocess,'run',side_effect=watch.subprocess.TimeoutExpired('curl',35)) as run:
            with self.assertRaises(watch.subprocess.TimeoutExpired):watch.fetch_response('https://huggingface.co/api/models')
            self.assertEqual(run.call_args.kwargs['timeout'],35)

    def test_visible_text_ignores_scripts(self):
        parser=watch.VisibleText(); parser.feed('<h1>Release</h1><script>fake model</script><p>2026-10-15</p>')
        self.assertEqual(parser.parts,['Release','2026-10-15'])

    def test_primary_and_additional_publishers_are_checked_once(self):
        with tempfile.TemporaryDirectory() as directory:
            topic=Path(directory)
            (topic/'src').mkdir()
            (topic/'src/release_watch.json').write_text(json.dumps({'checkedTeams':[
                {'team':'meta','hfOrg':'meta-llama','hfAdditionalOrgs':['meta-models','meta-llama','meta-models']}
            ]}))
            def inspect(job, *unused):
                return {'key':job[0], 'team':job[4], 'kind':job[3], 'status':'fetched'}
            with patch.object(watch,'TOPIC',topic), patch.object(watch,'ADDITIONAL_PAGES',{}), \
                 patch.object(watch,'fetch_job',side_effect=inspect) as fetch, \
                 patch('sys.argv',['check_base_model_releases.py','--previous',str(topic)]), contextlib.redirect_stdout(io.StringIO()):
                watch.main()
            keys=[call.args[0][0] for call in fetch.call_args_list]
            self.assertCountEqual(keys,['meta-llama','collections-meta-llama','meta-models','collections-meta-models','blog-meta'])


if __name__=='__main__':unittest.main()
