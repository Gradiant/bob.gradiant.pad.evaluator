from bob.gradiant.pad.evaluator.classes.dummies.dummy_access import DummyAccess
from bob.gradiant.core import Database, TypeDatabase, AccessModificator


class DummyDatabase(Database):

    def __init__(self, base_path, type_database=TypeDatabase.SPLIT, annotation_base_path=None):
        self.base_path = base_path
        super(DummyDatabase, self).__init__(base_path,
                                            type_database=TypeDatabase.ALL_FILES_TOGETHER,
                                            annotation_base_path=annotation_base_path)

    def __str__(self, name='Database'):
        return super(DummyDatabase, self).__str__(name=self.__class__.__name__)

    @staticmethod
    def name():
        return 'dummy-database'

    @staticmethod
    def is_a_collection_of_databases():
        return False

    @staticmethod
    def info():
        dict_info = { 'users' : 3,
                      'Train samples' : 2,
                      'Dev samples': 2,
                      'Test samples': 2}
        return dict_info

    def get_all_accesses(self, access_modificator=AccessModificator()):
        dict_all_accesses = {}
        list_accesses = []
        dict_accesses_by_subset = self.get_accesses_by_subset(access_modificator)
        for subset in dict_accesses_by_subset:
            list_accesses += dict_accesses_by_subset[subset]
        list_accesses.sort(key=lambda x: x.name)
        dict_all_accesses['All'] = list_accesses

    def get_accesses_by_subset(self, access_modificator=AccessModificator()):
        dict_accesses_by_subset = {}
        for subset in ['Train', 'Dev', 'Test']:
            list_accesses = []
            for number_access in range(0, 5):
                list_accesses.append(DummyAccess('base_path',
                                                 'real_' + str(number_access),
                                                 access_modificator=access_modificator))
            for number_access in range(0, 5):
                list_accesses.append(DummyAccess('base_path', 'attack_' + str(number_access),
                                                 access_modificator=access_modificator))
            list_accesses.sort(key=lambda x: x.name)
            dict_accesses_by_subset[subset] = list_accesses
        return dict_accesses_by_subset

    def get_attack_dict(self):
        return {'real': 0, 'attack': 1}

    def get_subsets(self):
        return ['Train', 'Dev', 'Test']

    def get_protocols(self):
        return ['grandtest']

    def get_ground_truth(self, protocol):
        dict_files = {}
        for subset in ['Train', 'Dev', 'Test']:
            dict_subset = {}
            for number_access in range(0, 5):
                dict_subset['real_' + str(number_access)] = self.get_attack_dict()['real']
            for number_access in range(0, 5):
                dict_subset['attack_' + str(number_access)] = self.get_attack_dict()['attack']
            dict_files[subset] = dict_subset
        return dict_files
