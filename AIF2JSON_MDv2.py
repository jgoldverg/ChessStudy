import json
import os
from collections import OrderedDict
import numpy as np
import pickle

def BatchPickle(Directory, Encoding='utf8'):
    for fname in os.listdir(Directory):
        if os.path.splitext(fname)[1].lower() == '.aif':
            print(fname)
            PickleAIF(os.path.join(Directory, fname), Encoding)

def PickleAIF(Filename, Encoding='utf8'):
    (Games, Moves) = ReadAIF(Filename, Encoding)
    (Games, Moves) = AIF2DICTv1(Games, Moves)
    pickle.dump(OrderedDict(zip(['Games', 'Moves'], [Games, Moves])), open(os.path.splitext(Filename)[0] + '.p', "wb" ))

# Converts the (Games, Moves) Pair to Standard Dictionary Pair
def AIF2DICTv1(AifGames, AifMoves):
    def SA(D, F):
        return (lambda: None, lambda: D[F])[F in D.keys()]()
    Games = []
    Moves = []
    for G in AifGames:
        game = OrderedDict()
        # Global Properties
        game['Global'] = OrderedDict()
        game['Global']['GameID'] = SA(G, 'GameID')
        game['Global']['ObjectType'] = 'Game'
        game['Global']['ObjectVersion'] = '0.2'
        # Compute Properties
        game['Compute'] = OrderedDict()
        game['Compute']['Engine'] = SA(G, 'EngineID')
        game['Compute']['Platform'] = SA(G, 'Platform')
        game['Compute']['Threads'] = SA(G, 'Threads')
        game['Compute']['Hash'] = SA(G, 'Hash')
        game['Compute']['MultiPV'] = SA(G, 'MultiPV')
        game['Compute']['Depths'] = SA(G, 'DepthRange')
        game['Compute']['EGT'] = SA(G, 'EGT')
        game['Compute']['Mode'] = SA(G, 'Mode')
        # Event Properties
        game['Event'] = OrderedDict()
        game['Event']['Name'] = SA(G, 'Event')
        game['Event']['Category'] = SA(G, 'EventCategory')
        game['Event']['Type'] = SA(G, 'EventType')
        game['Event']['Country'] = SA(G, 'EventCountry')
        game['Event']['Site'] = SA(G, 'Site')
        game['Event']['Date'] = SA(G, 'EventDate')
        game['Event']['Rounds'] = SA(G, 'EventRounds')
        # Game Properties
        game['Game'] = OrderedDict()
        game['Game']['White'] = OrderedDict()
        game['Game']['White']['Name'] = SA(G, 'White')
        game['Game']['White']['Elo'] = SA(G, 'WhiteElo')
        game['Game']['White']['Team'] = SA(G, 'WhiteTeam')
        game['Game']['White']['TeamCountry'] = SA(G, 'WhiteTeamCountry')
        game['Game']['Black'] = OrderedDict()
        game['Game']['Black']['Name'] = SA(G, 'Black')
        game['Game']['Black']['Elo'] = SA(G, 'BlackElo')
        game['Game']['Black']['Team'] = SA(G, 'BlackTeam')
        game['Game']['Black']['TeamCountry'] = SA(G, 'BlackTeamCountry')
        game['Game']['Date'] = SA(G, 'Date')
        game['Game']['EventRound'] = SA(G, 'Round')
        game['Game']['Victor'] = {'0-1': 'Black', '1-0': 'White', '1/2-1/2': 'Draw', None : None}[SA(G, 'Result')]
        game['Game']['Plys'] = SA(G, 'PlyCount')
        game['Game']['OpenECO'] = SA(G, 'ECO')
        game['Game']['StandardAlgebraic'] = SA(G, 'SAN')
        # Source Properties
        game['Source'] = OrderedDict()
        game['Source']['Source'] = SA(G, 'Source')
        game['Source']['Date'] = SA(G, 'SourceDate')
        Games.append(game)
    for M in AifMoves:
        move = OrderedDict()
        # Global Properties
        move['Global'] = OrderedDict()
        move['Global']['GameID'] = SA(G, 'GID')
        move['Global']['ObjectType'] = 'Move'
        move['Global']['ObjectVersion'] = '0.2'
        # Compute Properties
        move['Compute'] = OrderedDict()
        move['Compute']['Engine'] = SA(M, 'EID')
        move['Compute']['Depth'] = SA(M, 'Depth')
        move['Compute']['Nodes'] = SA(M, 'Nodes')
        # Move Properties
        move['Move'] = OrderedDict()
        move['Move']['Turn'] = M['Turn'].split('-')[0]
        move['Move']['Color'] = {'w': 'White', 'b': 'Black'}[M['Turn'].split('-')[1]]
        move['Move']['Played'] = M['MovePlayed']
        # Evaluation Properties
        move['Evaluation'] = OrderedDict()
        move['Evaluation']['Optimal'] = M['EngineMove']
        move['Evaluation']['Last'] = (lambda: str(int(M['PrevEval'])), lambda: None)[M['PrevEval'] == 'n.a.']()
        move['Evaluation']['This'] = str(int(M['Eval']))
        move['Evaluation']['Next'] = (lambda:str(int(M['NextEval'])), lambda: None)[M['NextEval'] == 'n.a.']()
        # Values Properties
        move['Values'] = OrderedDict()
        move['Values']['Identities'] = OrderedDict(zip(M['Values']['Identities'], list(range(len(M['Values']['Identities'])))))
        move['Values']['Matrix'] = np.array(M['Values']['Matrix'], dtype=np.float32)
        # Move Properties (contd.)
        move['Move']['Value'] = str(float(move['Values']['Matrix'][move['Values']['Identities'][move['Move']['Played']], -1]))
        # State Properties
        move['State'] = OrderedDict()
        move['State']['FEN'] = SA(M, 'FEN')
        move['State']['50MR'] = SA(M, 'FiftyMR')
        move['State']['Repetitions'] = OrderedDict()
        move['State']['Repetitions']['Count'] = SA(M, 'RepCount')
        move['State']['Repetitions']['OneToRep'] = SA(M, 'RepLine1')
        move['State']['Repetitions']['TwoToRep'] = SA(M, 'RepLine2')
        move['State']['Legal'] = OrderedDict()
        move['State']['Legal']['Count'] = SA(M, 'NumLegalMoves')
        move['State']['Legal']['Moves'] = SA(M, 'LegalMoves')
        # LAN Properties
        move['LAN'] = OrderedDict()
        move['LAN']['EnginePlayed'] = SA(M, 'EngineMoveLAN')
        move['LAN']['PlayerPlayed'] = SA(M, 'MovePlayedLAN')
        Moves.append(move)
    return (Games, Moves)

def ReadAIF(Filename, Encoding='utf8'):
    
    # Read AIF File Into Lines and Strip Whitespace
    lines = [line.rstrip() for line in open(Filename, encoding=Encoding, errors='ignore')]

    # Dictionary Records
    Games = []
    Moves = []

    # Working Items
    currGame = None
    currMove = None
    lastMove = None

    # Counter
    W = 0

    # Loop
    for I, L in enumerate(lines):
        
        # Manage Counters
        if W > 0:
            W -= 1
            continue

        # Blank Line Skip
        if len(L) == 0:
            continue
        
        # Comment Skip
        if L[0] == ';':
            continue

        # COND Open New Game Entry
        if (currGame is None) and (L[0:7] == '[GameID'):
            currGame = OrderedDict()
            currGame['ObjectType'] = 'Game'
            field = L[1:-2].split('"', 1)[0].strip()
            content = L[1:-2].split('"', 1)[1]
            currGame[field] = content
            continue
        
        # COND Append KV-Pair to Game Entry
        if (currGame is not None) and (L[0] == '['):
            field = L[1:-2].split('"', 1)[0].strip()
            content = L[1:-2].split('"', 1)[1]
            currGame[field] = content
            continue
        
        # COND Close Game Entry
        if (currGame is not None) and (L[0] != '['):
            currGame['GameSAN'] = L
            Games.append(currGame)
            currGame = None
        
        # COND Open New Move Entry
        if (currMove is None) and (L[0:4] == '[GID'):
            currMove = OrderedDict()
            currMove['ObjectType'] = 'Move'
            field = L[1:-2].split('"', 1)[0].strip()
            content = L[1:-2].split('"', 1)[1]
            currMove[field] = content
            continue

        # COND Append KV-Pair to Move Entry
        if (currMove is not None) and (L[0] == '['):
            field = L[1:-2].split('"', 1)[0].strip()
            content = L[1:-2].split('"', 1)[1]
            currMove[field] = content
            continue
        
        # COND Detect and Skip Value Grid Header
        if (currMove is not None) and (L[0] == '-') and (lines[I+1][0] == ' ') and (lines[I+2][0] == '-'):
            W = 2
            currMove['Values'] = OrderedDict()
            currMove['Values']['Identities'] = []
            currMove['Values']['Matrix'] = []
            continue

        # COND Read Value Grid Line
        if (currMove is not None) and (L[0] != '='):
            # Process Move
            mvect = list(filter(None, L.split(' ')))
            mname = mvect[0].strip()
            mvals = mvect[1:]
            # Heuristically Fill in Bad Values
            # Estimation Heuristic [Take From Prior]
            if lastMove is not None:
                mvals = [(cur, pri)[cur in ['PRUN', 'n.a.', 'NREC']] for cur, pri in zip(mvals, lastMove)]
            # Estimation Heuristic [Take From Left]
            evals = []
            elast = None
            for v in mvals:
                evals += [(v, elast)[(elast is not None) and (v in ['PRUN', 'n.a.', 'NREC'])]]
                elast = (v, elast)[v in ['PRUN', 'n.a.', 'NREC']]
            mvals = evals
            # Estimation Heuristic [Take From Right]
            evals = []
            elast = None
            for v in mvals[::-1]:
                evals += [(v, elast)[(elast is not None) and (v in ['PRUN', 'n.a.', 'NREC'])]]
                elast = (v, elast)[v in ['PRUN', 'n.a.', 'NREC']]
            mvals = evals[::-1]
            # Convert Numerics to Standard Format
            # Add '-' to Strings Ending in 'x' and Replace 'x'/'X' with '0'
            mvals = [(x, '-' + x)[x[-1] == 'x'].replace('x', '0').replace('X', '0') for x in mvals]
            # Add '-' to Strings Ending in 'c' and Replace 'c'/'C' with '00'
            mvals = [(x, '-' + x)[x[-1] == 'c'].replace('c', '00').replace('C', '00') for x in mvals]
            # Replace Strings as +M## with 100000-## and -M## with -100000+##
            mvals = [str((lambda: x, lambda: eval(x[0] + '(100000 - ' + x[2:].lstrip('0') + ')'))[x[1] == 'M']()) for x in mvals]
            mvals = [str((lambda: x, lambda: eval('(100000 - ' + x[1:].lstrip('0') + ')'))[x[0] == 'M']()) for x in mvals]
            mvals = [str((lambda: x, lambda: eval('(-100000 + ' + x[1:].lstrip('0') + ')'))[x[0] == 'm']()) for x in mvals]
            # Convert to Integers
            lastMove = mvals
            mvals = [int(x) for x in mvals]
            currMove['Values']['Identities'].append(mname)
            currMove['Values']['Matrix'].append(mvals)
            continue
        
        # COND Close Move
        if (currMove is not None) and (L[0] == '='):
            Moves.append(currMove)
            lastMove = None
            currMove = None
        
    return (Games, Moves)