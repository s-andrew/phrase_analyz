import math
import logging
from collections import namedtuple
from typing import List, Dict, Tuple

import numpy as np
from sklearn.linear_model import LogisticRegression

Rank = namedtuple('Rank', 'id left right')
Feature = namedtuple('Feature', 'coef grams')
RiskGroup = namedtuple('RiskGroup', 'id description action')

logger = logging.getLogger(__name__)


class CrossModel:
    def __init__(self):
        self.cross_matrix: Dict[Tuple[int, int], str] = None
        self.risk_groups: Dict[str, RiskGroup] = None
        self.basic: PredictModel = None
        self.combine: PredictModel = None
        return

    @staticmethod
    def fromDict(dictionary: dict) -> CrossModel:
        cm = CrossModel()
        cm.basic = PredictModel.fromDict(dictionary['basic'])
        cm.combine = PredictModel.fromDict(dictionary['combine'])
        cm.cross_matrix = dict(map(lambda x: ((x['basicRankId'], x['combineRankId']), x['riskGroupId']),
                                   dictionary['crossMatrix']))
        cm.risk_groups = dict(map(lambda x: (x['id'], RiskGroup(x['id'], x['description'], x['action'])),
                                  dictionary['riskGroups']))
        return cm

    def getRiskGroup(self, grams_keys: List[str]):
        logger.debug(msg='Grams keys = {}'.format(grams_keys))
        basic_vector = self.basic.createModelVectorByGramsKeys(grams_keys)
        logger.debug(msg='Basic vector = {}'.format(basic_vector))
        combine_vector = self.combine.createModelVectorByGramsKeys(grams_keys)
        logger.debug(msg='Combine vector = {}'.format(combine_vector))
        basic_rank = self.basic.getRank(basic_vector)
        combine_rank = self.combine.getRank(combine_vector)
        risk_group_id = self.cross_matrix[(basic_rank, combine_rank)]
        return self.risk_groups[risk_group_id]


class PredictModel:
    def __init__(self):
        self.default_rank: Rank = None
        self.ranks: List[Rank] = None
        self.features: List[Feature] = None
        self.model: LogisticRegression = None
        return

    @staticmethod
    def fromDict(dictionary: dict) -> PredictModel:
        pm = PredictModel()
        pm.rank = [Rank(r['id'],
                        -math.inf if r['left'] is None else r['left'],
                        math.inf if r['right'] is None else r['right'])
                   for r in dictionary['ranks']]
        pm.features = [Feature(f['coef'], f['grams']) for f in dictionary['features']]
        pm.default_rank = Rank(dictionary['defaultRank']['id'],
                               dictionary['defaultRank']['left'],
                               dictionary['defaultRank']['right'])
        pm.model = LogisticRegression()
        pm.model.coef_ = np.array([f.coef for f in pm.features])
        pm.model.intercept_ = np.array([dictionary['intercept']])
        pm.model.classes_ = np.array([0, 1], dtype='int8')
        return pm

    @staticmethod
    def in_feature(feature: Feature, gram_key: str) -> bool:
        for gram in feature.grams:
            if gram_key == gram:
                return True
        return False

    @staticmethod
    def any_in_feature(feature: Feature, grams_keys: List[str]):
        return any(map(lambda x: PredictModel.in_feature(feature, x), grams_keys))

    def createModelVectorByGramsKeys(self, grams_keys: List[str]):
        return [int(PredictModel.any_in_feature(feature, grams_keys)) for feature in self.features]

    def getRank(self, vector: List[int]):
        if all(map(lambda x: x==0, vector)):
            return self.default_rank
        X = np.array(vector).reshape(1, -1)
        descision_function = self.model.decision_function(X)
        for rank in self.ranks:
            if rank.left < descision_function <= rank.right:
                return rank.id
        return self.default_rank.id
