
def library_response(library):
  response = {'cards': len(library.cards)}
  
  if library.top_revealed:
    response['top'] = library.cards[0].to_dict()
    print 'ok'
  
  return response