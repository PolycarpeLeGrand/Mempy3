from mempy3.preprocess.docmodel import DocModel
from mempy3.config import DOCMODELS_PATH
from mempy3.utils.timer import Timer
import pandas as pd


def docmodel_read_speed_test(dm_path=DOCMODELS_PATH, max=1000000):
    print('Testing docmodel read speed')
    timer = Timer()
    for i, dm in enumerate(DocModel.docmodel_generator(dm_path)):
        t = dm.to_dict()
        if (i+1) == max:
            break
    print(f'Dm read speed test done. Read title from {max} docmodels in {timer.get_run_time()}')


def docmodel_tolist_speed_test(dm_path=DOCMODELS_PATH):
    print('Testing docmodel tolist speed')
    timer = Timer()
    r = [dm.metadata_to_dict() for dm in DocModel.docmodel_generator(dm_path)]
    print(f'Dm tolist speed test done. Made list with ids from {len(r)} docmodels in {timer.get_run_time()}')


def corpusframe_test(dm_path=DOCMODELS_PATH, max=1000):
    print('Testing corpusframe from dicts')
    timer=Timer()
    dl = [dm.to_dict() for i, dm in enumerate(DocModel.docmodel_generator(dm_path)) if i < max]
    df = pd.DataFrame(dl).set_index('id')
    print(f'Done making df from dicts, size: {df.memory_usage(index=True).sum()/(1024**2)} mbs')
    timer.step()
    print(df)


if __name__ == '__main__':
    corpusframe_test()


