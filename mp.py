from we7dm.util.commonDM import systemInit
systemInit()

import we7dm.config
import we7dm.recsys.configs
from we7dm.databases.offline import DmDatabase
from we7dm.recsys import ui
from we7dm.recsys.ui import filtering
from we7dm.recsys.predictors.pop import PopPredictor
from we7dm.recsys import similarity
from we7dm import optimizers
from we7dm.recsys.evaluation import evaluators

confidence_params_grid = {
    'predictor.item2item.similarityMeasureType': ['pairwise lift'],
    'predictor.item2item.minUserSupport': [0, 1, 2, 5],
    'predictor.item2item.minItemSupport': 2,
    'predictor.item2item.minItemConsumption': 2,  # 1 best for lift, 4 for conf
    'predictor.item2item.useUserNormalization': True, # just better,
    'predictor.item2item.useItemNormalization': False, # conf = lift is True,
    'predictor.item2item.commonCntMin': [0, 2, 5, 10, 20, 40, 60] # does it plateau after 80 for lift?,
    }

pop_params_grid = {'predictor.class': PopPredictor}

similarity_params_grid = {
    'predictor.item2item.similarityMeasureType': similarity.func_by_name.keys(),
    'predictor.item2item.minUserSupport': 0,
    'predictor.item2item.minItemSupport': 10,
    'predictor.item2item.minItemConsumption': 5,
    'predictor.item2item.useUserNormalization': True,
    'predictor.item2item.useItemNormalization': False,
    'predictor.item2item.commonCntMin': 50,
    }

params_to_evaluate = optimizers.generate_params_from_grids(
    search_grids=[pop_params_grid, confidence_params_grid, similarity_params_grid],
    default_params=we7dm.recsys.configs.config_dict)

print "%i params to evaluate" % (len(params_to_evaluate),)

test_topn = we7dm.config.get_test_recall_at()
predictor_evaluator = evaluators.PredictorEvaluator.from_uis(
    test_topn, ui_train, ui_test,
    users_with_history_only=we7dm.config.get_test_users_with_history_only(),
    allow_history_predictions=we7dm.config.get_test_allow_history_predictions(),
    metric_names=['recall', 'pop_discounted_recall', 'precision', 'AUC', 'GlobalItemCounter'])

