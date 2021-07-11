
import multiprocessing as mp, spacy, statistics, textblob as tb, tqdm
from collections import namedtuple
from pprint import pprint
from typing import Dict, Tuple

emoji_commands = dict({
  'cat': set(['🐈', '🐱', '🙀', '😾', '😿', '😼', '😺', '😹', '😸', '😽', '😻']),
  'cd': set(['🗄', '🗂']),
  'cp': set(['📋']),
  'free': set(['🆓']),
  'head': set(['🔝', '🆙']),
  'ls': set(['📝', '📜']),
  'mkdir': set(['📁','📂', '🖿']),
  'mv': set(['✂️', '🔪', '🗡️', ]),
  'nano': set(['🖊️', '🖋️', '✒️', '✍️']),
  'pwd': set(['⚓', '🗺️', '📍', '🧭']),
  'rm': set(['🧽', '🧹', '🧼']),
  'ssh': set(['🐚', '🐌', '🐢', '🦪']),
  'tail': set(['🔽', '⏬', '⬇️'])
})

def translate_emoji(emoji: str):
  """
  Get valid command from emoji.

  Parameters:
    emoji (str): Emoji to interpret.

  Returns:
    str: Valid Linux command from emoji. Invalid emoji will return None.
  """  
  for key, value in emoji_commands.items():
    if emoji in value:
      return key

  raise ValueError(f'The emoji \'{emoji}\' is not valid for any command.')

natural_language_commands = dict({
  'cat': set([
    'print out',
    'print',
    'display',
  ]),
  'cd': set([
    'change directory',
    'change folder',
    'change path',
    'change location'  
  ]),
  'cp': set([
    'copy',
    'copy items',
    'copy objects',
    'copy things'
    'make copies'
  ]),
  'free': set([
    'free memory',
    'need more memory',
    'release memory',
    'decrease memory usage'
  ]),
  'head': set([
    'get head',
    'get head of file',
    'top rows',
    'top portion of data',
    'display only top rows',
    'display only top data'
  ]),
  'ls': set([
    'list items',
    'list files',
    'show current directory contents',
    'get current items'
  ]),
  'mkdir': set([
    'make directory',
    'make folder',
    'make new directory',
    'make new folder',
    'create directory',
    'create folder',
    'create new directory',
    'create new folder'
  ]),
  'mv': set([
    'move',
    'move item',
    'move items',
    'move directory',
    'move directories',
    'move folders',
    'change item location'
  ]),
  'nano': set([
    'open text file',
    'edit text file'
  ]),
  'rm': set([
    'remove item',
    'remove files',
    'remove directory',
    'remove folder'
  ]),
  'pwd': set([
    'where am I',
    'current location',
    'what is my location',
    'what is the current location',
    'what is the current path',
    'what directory am I in'
  ]),
  'ssh': set([
    'secure shell',
    'secure login',
    'securely login'
    'login with IP address'
  ]),
  'tail': set([
    'print only bottom rows',
    'display bottom rows',
    'display last section of data',
    'show only lower portion of data'
  ])
})

Scores = namedtuple('Scores', ['maximum', 'median', 'mean'])

nlp = spacy.load('en_core_web_md')
def compute_sent_similarities_by_command(sentence: str, command: str):
  """
  Use document similarity function from Spacy to compute similarity scores between user-given sentence and all training sentences for that command.

  Parameters:
    sentence (str): User-given sentence.
    command (str): Command used as key to store set of training sentences.

  Returns:
    Tuple[str, float]: Tuple of command and similarity score.
  """
  if command not in natural_language_commands:
    raise ValueError(f'The command \'{command}\' is not registered.')

  sent = nlp(sentence)
  pool = mp.Pool(processes=8)
  similarity_scores = list([sent.similarity(nlp(sent_train)) for sent_train in natural_language_commands])
  scores = Scores(
    maximum=max(similarity_scores),
    median=statistics.median(data=similarity_scores),
    mean=statistics.mean(data=similarity_scores)
  )

  return command, scores

def compute_sent_similarities_all(sentence: str):
  """
  Compute dictionary of similariy scores between user-given sentence and all training sentences across hard-coded commands. Similarity scores are keyed or grouped by those commands. Each Scores instance for a command actually contains three (3) separate parts: maximum, median, and mean scores over all training sentences under that command.

  Parameters:
    sentence (str): User-given sentence.

  Returns:
    Dict[str, Scores]: Dictionary of similarity scores between user-given sentence and training sentences.
  """
  sent = nlp(sentence)
  pool = mp.Pool(processes=mp.cpu_count())
  scores_dict = dict(pool.starmap(func=compute_sent_similarities_by_command, iterable=[(sentence, command) for command in natural_language_commands]))
  
  return scores_dict



if __name__ == '__main__':
  sentence = 'where am I located'
  command, scores = compute_sent_similarities_by_command(sentence=sentence, command='pwd')
  pprint(command)
  pprint(scores)
  # score_dict = compute_sent_similarities_all(sentence=sentence)