###################################################################################################
#  Written by Selvin Cephus Jayakumar
###################################################################################################
import re
import torch
from SPARQLWrapper import SPARQLWrapper, JSON

import torch.nn as nn
import torch.nn.functional as F

from data_preprocess import DataPrep

MAX_LENGTH = 50
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

SOS_token = 0
EOS_token = 1

class EncoderRNN(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(EncoderRNN, self).__init__()
        self.hidden_size = hidden_size

        self.embedding = nn.Embedding(input_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size)

    def forward(self, input, hidden):
        embedded = self.embedding(input).view(1, 1, -1)
        output = embedded
        output, hidden = self.gru(output, hidden)
        return output, hidden

    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size, device=device)

class DecoderRNN(nn.Module):
    def __init__(self, hidden_size, output_size):
        super(DecoderRNN, self).__init__()
        self.hidden_size = hidden_size

        self.embedding = nn.Embedding(output_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size)
        self.out = nn.Linear(hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input, hidden):
        output = self.embedding(input).view(1, 1, -1)
        output = F.relu(output)
        self.gru.flatten_parameters()
        output, hidden = self.gru(output, hidden)
        output = self.softmax(self.out(output[0]))
        return output, hidden

    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size, device=device)

class AttnDecoderRNN(nn.Module):
    def __init__(self, hidden_size, output_size, dropout_p=0.1, max_length=MAX_LENGTH):
        super(AttnDecoderRNN, self).__init__()
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.dropout_p = dropout_p
        self.max_length = max_length

        self.embedding = nn.Embedding(self.output_size, self.hidden_size)
        self.attn = nn.Linear(self.hidden_size * 2, self.max_length)
        self.attn_combine = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.dropout = nn.Dropout(self.dropout_p)
        self.gru = nn.GRU(self.hidden_size, self.hidden_size)
        self.out = nn.Linear(self.hidden_size, self.output_size)

    def forward(self, input, hidden, encoder_outputs):
        embedded = self.embedding(input).view(1, 1, -1)
        embedded = self.dropout(embedded)

        attn_weights = F.softmax(
            self.attn(torch.cat((embedded[0], hidden[0]), 1)), dim=1)
        attn_applied = torch.bmm(attn_weights.unsqueeze(0),
                                 encoder_outputs.unsqueeze(0))

        output = torch.cat((embedded[0], attn_applied[0]), 1)
        output = self.attn_combine(output).unsqueeze(0)

        output = F.relu(output)
        output, hidden = self.gru(output, hidden)

        output = F.log_softmax(self.out(output[0]), dim=1)
        return output, hidden, attn_weights

    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size, device=device)

dt_prep = DataPrep('eng', 'sparql', False, device)
input_lang, output_lang, pairs = dt_prep.prepareData()

hidden_size = 1024
encoder1 = EncoderRNN(input_lang.n_words, hidden_size).to(device)
attn_decoder1 = AttnDecoderRNN(hidden_size, output_lang.n_words, dropout_p=0.1).to(device)
encoder1 = torch.load('encoder_decoder/encoder1_minproc', map_location='cpu')
attn_decoder1 = torch.load('encoder_decoder/attn_decoder1_minproc', map_location='cpu')
# encoder1 = torch.load('encoder_decoder/encoder1_minproc')
# attn_decoder1 = torch.load('encoder_decoder/attn_decoder1_minproc')

def evaluate(encoder, decoder, sentence, max_length=MAX_LENGTH):
    with torch.no_grad():
        input_tensor = dt_prep.tensorFromSentence(input_lang, sentence)
        input_length = input_tensor.size()[0]
        encoder_hidden = encoder.initHidden()

        encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

        for ei in range(input_length):
            encoder_output, encoder_hidden = encoder(input_tensor[ei],
                                                     encoder_hidden)
            encoder_outputs[ei] += encoder_output[0, 0]

        decoder_input = torch.tensor([[SOS_token]], device=device)  # SOS

        decoder_hidden = encoder_hidden

        decoded_words = []
        decoder_attentions = torch.zeros(max_length, max_length)

        for di in range(max_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            decoder_attentions[di] = decoder_attention.data
            topv, topi = decoder_output.data.topk(1)
            if topi.item() == EOS_token:
                decoded_words.append('<EOS>')
                break
            else:
                decoded_words.append(output_lang.index2word[topi.item()])

            decoder_input = topi.squeeze().detach()

        return decoded_words, decoder_attentions[:di + 1]

def call_to_sparql_endpoint(query):
    # query = "SELECT DISTINCT ?n WHERE { <http://dbpedia.org/resource/Steinsee> dbo:maximumDepth ?n . }"
    print(query)
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    # sparql.setQuery(query)  # the previous query as a literal string

    # resp = sparql.query().convert()
    resp = sparql.query()
    resp_dict = resp.convert()
    value = resp_dict['results']['bindings']
    print('Subject       Predicate        Object')
    for index in range(len(value)):
        subject = value[index]['s']
        predicate = value[index]['p']
        object = value[index]['o']
        # print('{} {} {}'.format(subject, predicate, object))
        if index == 100:
            return True
        # for s, p, o in value[index].items():
        #    print('{} {} {}'.format(s, p, o))
    # print('Sparql query respone: ', value)


def evaluateAndShowAttention(input_sentence):
    input_sentence = dt_prep.normalizeString(input_sentence)
    # sparqliser = SparqlPostprocessing()
    output_words, attentions = evaluate(
        encoder1, attn_decoder1, input_sentence)
    print('input =', input_sentence)
    print('output =', ' '.join(output_words))
    sparql_output = ' '.join(output_words)
    # sparql_query = sparqliser.sparqilise(sparql_output)
    sparql_query = re.sub(r'\<EOS\>', '', sparql_output)
    call_to_sparql_endpoint(sparql_query)

evaluateAndShowAttention("Which comic characters are painted by Bill Finger?")