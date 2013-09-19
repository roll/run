import ipclight
from .request import Request
from .response import Response

class Encoder:
    
    #Public
       
    def encode(self, message):
        transport_message = self._make_transport_message(message)
        text_message = self._make_text_message(transport_message)
        return text_message

    #Protected
    
    #TODO: implement
    def _make_transport_message(self, message):
        message_type = self._get_message_type(message)
    
    def _make_text_message(self, transport_message):
        return self._transport_encoder.encode(transport_message)
   
    def _get_transport_message_class(self, message):
        if isinstance(message, Request):
            return ipclight.Request
        elif isinstance(message, Response):
            return ipclight.Response
        else:
            raise EncodeError('Message type error: '+str(type(message)))
        
    #TODO: use cached property
    @property
    def _transport_encoder(self):
        return ipclight.Encoder()
    
    
class EncodeError(Exception): pass     