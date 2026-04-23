import inspect
from langchain.chains import RetrievalQA

print('init', inspect.signature(RetrievalQA.__init__))
print('from_chain_type', inspect.signature(RetrievalQA.from_chain_type))
print(RetrievalQA.from_chain_type.__doc__)
