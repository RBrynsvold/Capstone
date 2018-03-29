from gensim.models.coherencemodel import CoherenceModel
from utils_streamers import DirFileMgr, CorpStreamer, BOWCorpStreamer
from gensim import corpora
from gensim.models.ldamodel import LdaModel
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)

dr_id_str = "dr_500k"
dr_fps = DirFileMgr(dr_id_str)
dr_fps.create_all_dr_fps(new_setup='N')

mod_id_str = "gpu_mod_run_1"
fps1 = DirFileMgr(mod_id_str)
fps1.create_all_modeling_fps(mod_id_str)
# fps1.add_fp('pyLDAvis')
fps1.add_fp('coherence_model')