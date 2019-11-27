import csv
import json
from unittest import TestCase
from unittest.mock import patch
from load_sample import load_sample


@patch('load_sample.RabbitContext')
class TestLoadSample(TestCase):

    def test_load_sample_publishes_case_to_rabbit(self, patch_rabbit):
        
        sample_file = (
            'ARID,ESTAB_ARID,UPRN,ADDRESS_TYPE,ESTAB_TYPE,ADDRESS_LEVEL,ABP_CODE,ORGANISATION_NAME,ADDRESS_LINE1,'
            'ADDRESS_LINE2,ADDRESS_LINE3,TOWN_NAME,POSTCODE,LATITUDE,LONGITUDE,OA,LSOA,MSOA,LAD,REGION,HTC_WILLINGNESS,'
            'HTC_DIGITAL,FIELDCOORDINATOR_ID,FIELDOFFICER_ID,TREATMENT_CODE,CE_EXPECTED_CAPACITY',
            'DDR190314000000195675,DDR190314000000113740,10008677190,HH,Household,U,RD06,,Flat 56 Francombe House,'
            'Commercial Road,,Windleybury,XX1 0XX,51.4463421,-2.5924477,E00073438,E01014540,E02003043,E06000023,'
            'E12000009,1,5,1,2,HH_LF3R2E,3',
            'DDR190314000000239595,DDR190314000000060908,10008677190,HH,Household,U,RD06,,First And Second Floor Flat,'
            '39 Cranbrook Road,,Windleybury,XX1 0XX,51.4721166,-2.5970579,E00074083,E01014669,E02003031,E06000023,'
            'E12000009,2,4,4,5,HH_LF3R3AE,6')

        load_sample(sample_file, 'test_ce_uuid', 'test_ap_uuid')

        patch_rabbit_context = patch_rabbit.return_value.__enter__.return_value

        self.assertEqual(2, patch_rabbit_context.publish_message.call_count)
        publish_message_call_args = patch_rabbit_context.publish_message.call_args_list

        self._check_published_cases_contain_required_data(publish_message_call_args, sample_file)

    def _check_published_cases_contain_required_data(self, publish_message_call_args, sample_file):
        sample_file_rows = csv.DictReader(sample_file)
        for row_number, sample_row in enumerate(sample_file_rows):
            message_contents = json.loads(publish_message_call_args[row_number][0][0])
            self.assertEqual(sample_row['ARID'], message_contents['arid'])
            self.assertEqual(sample_row['ADDRESS_LINE1'], message_contents['addressLine1'])
