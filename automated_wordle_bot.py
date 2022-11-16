from playwright.sync_api import sync_playwright
import time
from random import choice
from bs4 import BeautifulSoup

won_games = 0
lost_games = 0

WORDS = ['north', 'roach', 'spoof', 'areal', 'solar', 'bogey', 'gamey', 'affix', 'levee', 'bride', 'beret', 'ripen',
         'exile', 'usher', 'falls', 'trope', 'pieta', 'atoll', 'mirth', 'birth', 'pluck', 'caber', 'sling', 'allot',
         'amuse', 'belle', 'torch', 'wench', 'melon', 'tenor', 'roger', 'gauss', 'abohm', 'maund', 'razor', 'verst',
         'flick', 'frisk', 'bleep', 'jolly', 'bully', 'meaty', 'nerve', 'spoil', 'butte', 'swing', 'picul', 'greed',
         'clack', 'setup', 'posit', 'brail', 'noted', 'bible', 'nyala', 'munch', 'covey', 'saute', 'women', 'colic',
         'taunt', 'spunk', 'queue', 'shove', 'hasty', 'whirl', 'raver', 'taxer', 'crass', 'knell', 'brand',
         'madly', 'throe', 'dryer', 'oaken', 'swoon', 'bliss', 'sprue', 'gaunt', 'sabot', 'rowdy', 'apery', 'nadir',
         'voila', 'steam', 'fritz', 'aloes', 'white', 'might', 'cubby', 'decoy', 'assay', 'skink', 'apart', 'dolly',
         'envoy', 'alkyd', 'bathe', 'spool', 'whelk', 'pubis', 'gavel', 'naira', 'steak', 'lobar', 'carve', 'fable',
         'scrum', 'metro', 'areca', 'oldie', 'shape', 'plaid', 'steal', 'slide', 'abbot', 'havoc', 'shore', 'mural',
         'harem', 'churr', 'these', 'above', 'panic', 'droll', 'khaki', 'hewer', 'tempo', 'mufti', 'usury', 'charm',
         'rocky', 'pubic', 'tumid', 'grout', 'which', 'brave', 'radar', 'locus', 'vocal', 'apish', 'fauna', 'dicot',
         'fusty', 'noose', 'blini', 'calve', 'egret', 'latex', 'dodgy', 'tithe', 'hyper', 'focal', 'kraal', 'ichor',
         'bialy', 'sabra', 'odder', 'knead', 'mambo', 'laxly', 'verve', 'spiky', 'smuts', 'dregs', 'cliff', 'linin',
         'whack', 'prang', 'quasi', 'furry', 'silky', 'amiss', 'zloty', 'taint', 'trait', 'papaw', 'style', 'scram',
         'alive', 'spray', 'cling', 'glade', 'manes', 'dicer', 'messy', 'thumb', 'focus', 'jelly', 'bawdy', 'diver',
         'chick', 'bulla', 'debug', 'swore', 'false', 'corer', 'offal', 'haler', 'about', 'parer', 'brunt', 'scion',
         'meter', 'spell', 'privy', 'willy', 'ranch', 'mayor', 'boast', 'young', 'giddy', 'woody', 'ounce', 'sheet',
         'cheek', 'virus', 'batch', 'riper', 'fella', 'rough', 'butch', 'quoin', 'cense', 'salad', 'grass', 'imago',
         'fixer', 'mucor', 'smash', 'squaw', 'event', 'bloke', 'loamy', 'scene', 'femur', 'fleet', 'arson', 'dimer',
         'shirr', 'louis', 'boric', 'velar', 'amend', 'vivid', 'guard', 'dusty', 'derby', 'dress', 'murky', 'stock',
         'bleed', 'spare', 'rummy', 'patio', 'relax', 'bayou', 'meany', 'cadet', 'award', 'eying', 'deity', 'hinny',
         'tenon', 'rajah', 'syrup', 'ileum', 'blush', 'trove', 'acute', 'straw', 'donna', 'hoist', 'laser', 'vagus',
         'jimmy', 'swoop', 'loner', 'serow', 'drink', 'trace', 'suety', 'quark', 'bongo', 'emmer', 'buxom', 'hired',
         'shill', 'ratty', 'yenta', 'match', 'fossa', 'pinko', 'squab', 'peril', 'parts', 'evade', 'pipit', 'benny',
         'rupee', 'chyme', 'filet', 'whiny', 'drier', 'braze', 'codon', 'flats', 'spume', 'ovule', 'potty', 'cisco',
         'daisy', 'plead', 'surer', 'rival', 'thank', 'baron', 'snuff', 'niche', 'steel', 'rarer', 'truer', 'prone',
         'stood', 'vireo', 'thrum', 'cabin', 'umbel', 'sucre', 'mercy', 'tenge', 'copal', 'rodeo', 'rainy', 'flour',
         'toned', 'luffa', 'wimpy', 'sweat', 'chirr', 'issue', 'tooth', 'spite', 'musty', 'tempt', 'tenet', 'auxin',
         'sight', 'theme', 'peter', 'comet', 'virga', 'musky', 'missy', 'breed', 'cubeb', 'tasty', 'befit', 'tinea',
         'terce', 'aping', 'feria', 'gravy', 'frizz', 'hoard', 'cutin', 'clamp', 'sweep', 'molar', 'chair', 'blunt',
         'going', 'stomp', 'antsy', 'aloha', 'deist', 'nanny', 'softy', 'pizza', 'bloat', 'guyot', 'sylph', 'pitta',
         'fauve', 'worse', 'gaffe', 'annul', 'kopek', 'leone', 'again', 'sadhu', 'among', 'elite', 'opera', 'betel',
         'drunk', 'hooks', 'tuber', 'drone', 'sheen', 'idler', 'jenny', 'grebe', 'chufa', 'share', 'guise', 'dingy',
         'third', 'oread', 'mound', 'peaky', 'still', 'toque', 'seedy', 'inion', 'niece', 'gesso', 'troll', 'carry',
         'snook', 'spiff', 'leafy', 'crore', 'mongo', 'bored', 'droop', 'pouch', 'flint', 'thong', 'ample', 'craps',
         'ebony', 'wafer', 'fusil', 'shire', 'sower', 'xerox', 'black', 'caulk', 'alias', 'kappa', 'prick', 'raven',
         'lucky', 'titan', 'mourn', 'incur', 'ashen', 'built', 'stork', 'pence', 'carom', 'human', 'cutch', 'midge',
         'check', 'spoor', 't-man', 'taffy', 'wryly', 'sugar', 'raper', 'junta', 'twerp', 'fatso', 'filmy', 'nervy',
         'psalm', 'breve', 'aural', 'geese', 'mated', 'kafir', 'shrub', 'baggy', 'hilum', 'aroid', 'spicy', 'manat',
         'known', 'buyer', 'stink', 'magus', 'arose', 'fovea', 'ensue', 'dogma', 'tenth', 'thebe', 'grave', 'monad',
         'sweet', 'tubed', 'corps', 'wield', 'hussy', 'march', 'sigma', 'spank', 'hippo', 'ravel', 'dopey', 'scree',
         'robot', 'other', 'swept', 'hooch', 'quake', 'squad', 'flare', 'annex', 'champ', 'briny', 'baler', 'bursa',
         'leaky', 'prude', 'quart', 'board', 'level', 'equal', 'abuzz', 'baton', 'moody', 'rabid', 'poppy', 'dulse',
         'horde', 'bruin', 'kitty', 'piper', 'trail', 'segno', 'bolus', 'sixth', 'seven', 'twist', 'louse', 'cloud',
         'igloo', 'cecum', 'amain', 'winch', 'diazo', 'urial', 'tabby', 'soled', 'mauve', 'manky', 'dunce', 'knack',
         'metal', 'liger', 'pilot', 'links', 'scape', 'atilt', 'storm', 'vigil', 'tower', 'quiff', 'perry', 'naris',
         'ember', 'lapse', 'posed', 'thunk', 'lunge', 'ridge', 'weedy', 'udder', 'whine', 'domed', 'eater', 'groan',
         'vagal', 'grime', 'agent', 'bingo', 'solan', 'pried', 'croft', 'hater', 'giver', 'jumpy', 'stint', 'blame',
         'alley', 'cozen', 'wacky', 'algin', 'swung', 'exert', 'allow', 'inane', 'nexus', 'allyl', 'friar', 'durra',
         'audio', 'wedge', 'dingo', 'limey', 'early', 'phyle', 'servo', 'crust', 'unity', 'artsy', 'riser', 'medal',
         'finer', 'fleer', 'covet', 'spout', 'proof', 'track', 'clump', 'manna', 'baste', 'shaky', 'lefty', 'draft',
         'comma', 'entry', 'kayak', 'flack', 'warty', 'teary', 'queer', 'waist', 'heavy', 'mothy', 'gonad', 'snail',
         'telex', 'suing', 'thief', 'terse', 'joker', 'bosky', 'teens', 'clear', 'risen', 'medic', 'henry', 'fakir',
         'ditty', 'dicky', 'testy', 'tonic', 'genre', 'swage', 'macaw', 'frank', 'nylon', 'slate', 'halve', 'water',
         'sprig', 'helix', 'lapin', 'newsy', 'drake', 'obeah', 'gouge', 'stout', 'clone', 'evoke', 'thigh', 'dolce',
         'hedge', 'smoke', 'boxer', 'leper', 'elate', 'great', 'slack', 'twixt', 'avail', 'puffy', 'crane', 'stoat',
         'bones', 'babel', 'coven', 'comfy', 'salvo', 'unmet', 'order', 'negus', 'aptly', 'scuba', 'baiza', 'nosed',
         'enemy', 'roble', 'shade', 'vapid', 'ought', 'oakum', 'unset', 'filth', 'fight', 'snowy', 'silly', 'fence',
         'token', 'hajji', 'slush', 'unite', 'fresh', 'siege', 'debit', 'faced', 'chime', 'asper', 'gloat', 'liner',
         'hawse', 'squib', 'borne', 'geeky', 'naked', 'aider', 'fugal', 'gleam', 'coati', 'nawab', 'fault', 'bicep',
         'tulle', 'imply', 'rouse', 'bland', 'sinus', 'modem', 'logic', 'ninja', 'river', 'bedew', 'mafia', 'twins',
         'mucus', 'abuse', 'flies', 'dread', 'cauda', 'cavil', 'silva', 'lipid', 'cynic', 'slime', 'silty', 'cleat',
         'magic', 'scope', 'facet', 'dwelt', 'paean', 'union', 'brawl', 'aback', 'snaky', 'blink', 'pasha', 'aspic',
         'optic', 'prove', 'tiler', 'pacer', 'paisa', 'plait', 'solve', 'chard', 'argue', 'lathe', 'metis', 'racer',
         'gauge', 'youth', 'avian', 'pinto', 'vulva', 'posse', 'grant', 'snick', 'skirl', 'picot', 'ankle', 'snack',
         'renin', 'dinky', 'prate', 'habit', 'flung', 'rugby', 'dildo', 'lisle', 'decor', 'bally', 'midst', 'godly',
         'feint', 'jiffy', 'guide', 'grief', 'worry', 'unlit', 'drama', 'doped', 'burgh', 'swear', 'valid', 'snort',
         'limbo', 'bonny', 'equip', 'retry', 'torso', 'trunk', 'maria', 'usurp', 'psoas', 'basic', 'three', 'slope',
         'harpy', 'kneed', 'owned', 'poach', 'folio', 'wagon', 'spoke', 'acerb', 'sprit', 'otter', 'ideal', 'adapt',
         'lobed', 'biter', 'venue', 'parks', 'algae', 'revue', 'sable', 'moral', 'lumen', 'begat', 'salon', 'logan',
         'viper', 'pulse', 'glove', 'angle', 'monte', 'fives', 'arete', 'total', 'timed', 'davit', 'randy', 'sniff',
         'galea', 'vomit', 'croup', 'bight', 'guile', 'tayra', 'haste', 'incus', 'gypsy', 'klutz', 'manor', 'sunny',
         'gusty', 'dummy', 'acorn', 'etude', 'harry', 'chyle', 'prime', 'musth', 'gemma', 'irate', 'wager', 'price',
         'drift', 'plain', 'watch', 'viand', 'clung', 'recap', 'chaos', 'canoe', 'burst', 'cupid', 'limit', 'viral',
         'laden', 'cello', 'curio', 'blahs', 'video', 'reach', 'banns', 'recur', 'clown', 'gaudy', 'began', 'roads',
         'rheum', 'quell', 'leapt', 'borax', 'orbit', 'snood', 'realm', 'treat', 'ethyl', 'futon', 'anime', 'canto',
         'pudgy', 'flair', 'zaire', 'hover', 'bough', 'scary', 'heaps', 'grist', 'stave', 'zonal', 'mulch', 'piton',
         'sough', 'doing', 'sorus', 'runic', 'props', 'delay', 'phase', 'oddly', 'bugle', 'wreck', 'quill', 'pagan',
         'mangy', 'choke', 'juicy', 'deuce', 'douse', 'chide', 'blond', 'shake', 'darky', 'cocky', 'eland', 'fichu',
         'lotto', 'weepy', 'abbey', 'auger', 'aphid', 'mecca', 'franc', 'dusky', 'amino', 'latch', 'idiom', 'rumba',
         'smirk', 'cigar', 'place', 'cream', 'ethos', 'degas', 'oxide', 'sewed', 'evert', 'tying', 'using', 'zoril',
         'fatal', 'mason', 'loved', 'ester', 'inlay', 'sebum', 'clock', 'roast', 'break', 'hatch', 'liver', 'snore',
         'flail', 'pushy', 'crony', 'crime', 'knish', 'motet', 'detox', 'ketch', 'ivied', 'truly', 'creed', 'palsy',
         'await', 'flask', 'yield', 'whist', 'rivet', 'modal', 'colon', 'nobly', 'sixty', 'booby', 'pubes', 'flank',
         'route', 'doggo', 'cadre', 'seine', 'binge', 'write', 'ennui', 'motto', 'unman', 'usage', 'soupy', 'aedes',
         'dizzy', 'enema', 'tense', 'rifle', 'cornu', 'gammy', 'tiled', 'cabby', 'saint', 'rebel', 'steep', 'mania',
         'debar', 'phlox', 'rosin', 'burly', 'elbow', 'agape', 'carob', 'buteo', 'upend', 'bocce', 'meant', 'croon',
         'muser', 'remit', 'flesh', 'qibla', 'lance', 'swede', 'varix', 'glory', 'tabor', 'utter', 'welsh', 'numen',
         'bravo', 'bulky', 'bossy', 'splat', 'skier', 'avert', 'upper', 'worth', 'dilly', 'hypha', 'frost', 'curse',
         'terra', 'cargo', 'sadly', 'smelt', 'quits', 'trick', 'rebut', 'rogue', 'crawl', 'bison', 'broom', 'askew',
         'dealt', 'quaff', 'flown', 'femme', 'besom', 'kazoo', 'circa', 'hinge', 'dogie', 'conic', 'feral', 'clary',
         'pouty', 'synod', 'peaty', 'guppy', 'magma', 'ducat', 'peeve', 'graph', 'burin', 'knife', 'ovate', 'spiny',
         'caret', 'calyx', 'pixel', 'sepal', 'coast', 'basin', 'caste', 'lagan', 'lease', 'omega', 'major', 'milch',
         'honey', 'tabes', 'flume', 'fewer', 'theft', 'manse', 'drill', 'gross', 'no-go', 'fanny', 'civil', 'stoic',
         'super', 'gloss', 'drove', 'mealy', 'train', 'lotus', 'oxbow', 'house', 'paved', 'tepid', 'gofer', 'lapel',
         'xeric', 'spitz', 'teddy', 'butut', 'niffy', 'virtu', 'anger', 'final', 'renew', 'edict', 'smart', 'copra',
         'defer', 'foggy', 'dower', 'tinny', 'hurry', 'shown', 'clove', 'short', 'react', 'flunk', 'firth', 'tract',
         'urine', 'penal', 'newly', 'leery', 'disco', 'adult', 'brown', 'grown', 'alate', 'coact', 'fatty', 'elegy',
         'stool', 'spade', 'withe', 'graze', 'kanzu', 'afire', 'valet', 'strip', 'wally', 'carol', 'chafe', 'stray',
         'debut', 'prize', 'verge', 'chalk', 'cuddy', 'cramp', 'parry', 'tardy', 'inkle', 'sassy', 'pogge', 'pride',
         'couch', 'wages', 'squid', 'smile', 'vedic', 'brief', 'qualm', 'since', 'steed', 'lying', 'natal', 'piece',
         'haply', 'yodel', 'cinch', 'stunt', 'quail', 'shalt', 'viola', 'retie', 'couth', 'night', 'fifty', 'creep',
         'noble', 'hertz', 'pleat', 'month', 'yearn', 'middy', 'goody', 'recce', 'burke', 'serge', 'slang', 'beige',
         'maser', 'cuppa', 'crate', 'blurt', 'libel', 'tamed', 'namer', 'outdo', 'canny', 'henna', 'mudra', 'teach',
         'windy', 'tripe', 'ology', 'tweed', 'frame', 'fetus', 'crape', 'anile', 'terry', 'delft', 'blend', 'drank',
         'means', 'resew', 'wordy', 'potto', 'whizz', 'lever', 'voter', 'exact', 'villa', 'mucin', 'loopy', 'goose',
         'wheat', 'bribe', 'anima', 'erase', 'slick', 'bowel', 'neigh', 'spent', 'peace', 'bhang', 'copse', 'stare',
         'ukase', 'under', 'shine', 'plant', 'fairy', 'ploce', 'cacao', 'quipu', 'fiver', 'weary', 'verse', 'cache',
         'gouty', 'reuse', 'earth', 'theta', 'semen', 'thick', 'purer', 'anion', 'tarry', 'aglow', 'slave', 'swank',
         'wispy', 'ether', 'wirer', 'coupe', 'rhino', 'argon', 'koala', 'shady', 'noisy', 'risky', 'clink', 'naiad',
         'ohmic', 'jabot', 'knoll', 'unfed', 'tangy', 'relay', 'snake', 'costa', 'upset', 'first', 'grasp', 'creel',
         'sneak', 'divot', 'balas', 'pinon', 'shunt', 'lysis', 'uncle', 'inset', 'admin', 'belly', 'eared', 'knelt',
         'works', 'salsa', 'gumbo', 'aisle', 'inept', 'bread', 'bezel', 'title', 'dense', 'mooch', 'choir', 'abase',
         'cloth', 'green', 'sumac', 'grail', 'okapi', 'brain', 'libra', 'ficus', 'crepe', 'waive', 'throb', 'crack',
         'sabin', 'hound', 'scaly', 'mouth', 'greet', 'clews', 'sewer', 'puppy', 'guild', 'genic', 'shiny', 'comic',
         'alone', 'trump', 'plumb', 'mower', 'strap', 'flute', 'totem', 'spoon', 'ergot', 'botch', 'calla', 'zesty',
         'oiler', 'stilt', 'mamey', 'freak', 'zayin', 'amble', 'where', 'agora', 'skunk', 'putty', 'dowry', 'plonk',
         'wired', 'saiga', 'azure', 'indic', 'bunny', 'kauri', 'crake', 'frail', 'sorgo', 'wiser', 'sword', 'lexis',
         'valve', 'codex', 'swipe', 'slump', 'jaunt', 'golly', 'bring', 'trash', 'porgy', 'bract', 'd-day', 'flora',
         'sooth', 'music', 'onion', 'girly', 'mumps', 'bloom', 'jorum', 'boxed', 'drupe', 'stogy', 'admix', 'older',
         'adust', 'begum', 'cress', 'vicar', 'curry', 'flame', 'imide', 'poesy', 'recut', 'spied', 'penny', 'faint',
         'abaca', 'force', 'fluff', 'mulct', 'adobe', 'blood', 'octet', 'ulcer', 'eight', 'voice', 'leech', 'split',
         'prowl', 'croak', 'rusty', 'hefty', 'miler', 'piggy', 'manly', 'chore', 'denim', 'nasal', 'beamy', 'handy',
         'safer', 'ceiba', 'aalii', 'story', 'barge', 'stung', 'whomp', 'drain', 'grimy', 'hello', 'boost', 'sheep',
         'deism', 'stiff', 'holly', 'skulk', 'genet', 'abate', 'tansy', 'ghoul', 'party', 'scarf', 'nutty', 'gusto',
         'prism', 'avens', 'piano', 'enate', 'arced', 'adore', 'payer', 'watts', 'decay', 'swell', 'sprag', 'glide',
         'morse', 'glass', 'thill', 'cobia', 'aldol', 'close', 'slash', 'fixed', 'zamia', 'julep', 'educe', 'exist',
         'pansy', 'overt', 'shiva', 'flump', 'inlet', 'shell', 'scoop', 'cover', 'dutch', 'basil', 'tulip', 'flush',
         'esker', 'voile', 'death', 'flake', 'topaz', 'coral', 'banal', 'butyl', 'suave', 'group', 'porch', 'jural',
         'bless', 'snipe', 'snafu', 'ephah', 'elope', 'ruled', 'gummy', 'catch', 'daddy', 'oriel', 'morel', 'ritzy',
         'pooch', 'johns', 'dryly', 'bigot', 'nicer', 'dinge', 'sprat', 'lanai', 'frond', 'trade', 'hyoid', 'stale',
         'nones', 'serve', 'visor', 'begun', 'unify', 'phone', 'hijab', 'argil', 'druid', 'skeet', 'dairy', 'freed',
         'pommy', 'junco', 'dandy', 'claro', 'rapid', 'osier', 'dobra', 'plume', 'hydro', 'lowly', 'snoop', 'their',
         'budge', 'flout', 'outer', 'mince', 'spire', 'bushy', 'bovid', 'purge', 'fever', 'given', 'elute', 'drawn',
         'nidus', 'chewy', 'mixer', 'azide', 'penni', 'cleft', 'gripe', 'stalk', 'trawl', 'muggy', 'adieu', 'waxed',
         'stall', 'pedal', 'salmi', 'later', 'drawl', 'belie', 'cable', 'giant', 'tapir', 'cutie', 'prink', 'sulky',
         'roomy', 'aleph', 'lofty', 'xenon', 'broke', 'bacon', 'gamma', 'plaza', 'vodka', 'fucus', 'hexed', 'right',
         'ricer', 'satin', 'weave', 'bated', 'chuck', 'rayon', 'shout', 'those', 'talus', 'tubal', 'genip', 'widow',
         'pavis', 'sober', 'badge', 'berth', 'merry', 'braid', 'stash', 'banjo', 'wells', 'pecan', 'noria', 'timer',
         'jerky', 'horse', 'ulnar', 'gruel', 'cased', 'motor', 'fluid', 'trice', 'moist', 'after', 'alarm', 'regal',
         'tonal', 'minor', 'actor', 'emote', 'grate', 'nasty', 'miser', 'forum', 'huffy', 'tamer', 'bidet', 'chest',
         'crumb', 'depth', 'kraft', 'drown', 'afoul', 'gonif', 'strop', 'visit', 'jihad', 'knout', 'stove', 'angst',
         'wiper', 'suede', 'slice', 'v-day', 'perky', 'datum', 'repay', 'shoal', 'litas', 'ilium', 'yucca', 'hunky',
         'slake', 'birch', 'judge', 'kiosk', 'fungi', 'cloak', 'chase', 'spurt', 'redly', 'below', 'scalp', 'dirty',
         'gable', 'goner', 'dream', 'spice', 'arrow', 'sting', 'cider', 'non-u', 'salol', 'zooid', 'quash', 'lotic',
         'senna', 'scant', 'dryad', 'condo', 'inbox', 'awake', 'afoot', 'patsy', 'being', 'uncut', 'laird', 'mores',
         'biota', 'biped', 'axial', 'crump', 'grace', 'smoky', 'local', 'biddy', 'spasm', 'stony', 'downy', 'depot',
         'burro', 'funky', 'dicey', 'truce', 'chief', 'romeo', 'gourd', 'clean', 'mamma', 'stain', 'beset', 'capon',
         'reply', 'toxin', 'tepee', 'tweet', 'growl', 'scrim', 'sloth', 'front', 'mammy', 'pivot', 'wharf', 'embed',
         'ethic', 'serin', 'waver', 'eking', 'input', 'yahoo', 'revet', 'bleak', 'wrote', 'spall', 'lusty', 'fugue',
         'abeam', 'taped', 'beast', 'hilly', 'tammy', 'hours', 'koine', 'hands', 'houri', 'brace', 'swill', 'poser',
         'marks', 'sauce', 'livid', 'attar', 'pyxie', 'tetra', 'shoot', 'crept', 'heady', 'cruel', 'tiger', 'inter',
         'waste', 'scout', 'impel', 'augur', 'krill', 'lymph', 'prune', 'faith', 'roots', 'corgi', 'ootid', 'unpin',
         'opium', 'prose', 'segue', 'kinky', 'lanky', 'grill', 'point', 'every', 'glare', 'based', 'comer', 'cubic',
         'humph', 'ducal', 'scold', 'tilth', 'smith', 'cecal', 'pithy', 'chela', 'llama', 'kvass', 'moose', 'alkyl',
         'folks', 'buddy', 'pesky', 'ozone', 'image', 'groom', 'vixen', 'tunic', 'nabob', 'krait', 'eaten', 'leash',
         'stupa', 'label', 'heave', 'woken', 'smack', 'samba', 'sharp', 'sally', 'drape', 'donor', 'nisei', 'alloy',
         'woven', 'bling', 'diary', 'plane', 'aside', 'asset', 'excel', 'metic', 'mange', 'fryer', 'guano', 'girth',
         'floss', 'weigh', 'polka', 'laugh', 'stair', 'erode', 'tired', 'dirge', 'weeds', 'amply', 'glyph', 'jawed',
         'glean', 'delta', 'seize', 'zebra', 'poilu', 'hairy', 'slept', 'crier', 'blare', 'cheat', 'grind', 'muddy',
         'brush', 'tiara', 'lucid', 'rider', 'ramie', 'curly', 'scone', 'woman', 'anode', 'tweak', 'brass', 'stead',
         'kiang', 'briar', 'quilt', 'audit', 'guess', 'nurse', 'drive', 'pixie', 'staid', 'heard', 'skimp', 'payee',
         'husky', 'paler', 'deify', 'gulag', 'frock', 'mocha', 'maize', 'thorn', 'gorse', 'juror', 'idiot', 'addle',
         'abide', 'rings', 'fancy', 'naval', 'haunt', 'evict', 'robin', 'skull', 'bluff', 'error', 'chirp', 'cushy',
         'naive', 'cagey', 'retro', 'hoary', 'llano', 'plate', 'hiker', 'civic', 'dekko', 'humic', 'duchy', 'spill',
         'filly', 'taper', 'swift', 'media', 'hutch', 'never', 'chunk', 'photo', 'clash', 'bulge', 'strum', 'roman',
         'camel', 'quirt', 'soave', 'ovoid', 'exalt', 'tried', 'pinch', 'blowy', 'primo', 'ratio', 'ferry', 'blurb',
         'oxime', 'money', 'vower', 'crisp', 'slosh', 'lynch', 'wight', 'bunch', 'bilge', 'aphis', 'triad', 'smote',
         'hotly', 'while', 'slyly', 'spiel', 'chart', 'senor', 'taupe', 'shush', 'genoa', 'pound', 'heist', 'blast',
         'jacks', 'trust', 'negro', 'twice', 'widen', 'tango', 'favus', 'holey', 'saury', 'corny', 'hence', 'crush',
         'marly', 'shuck', 'quire', 'eosin', 'loess', 'fleck', 'index', 'eaves', 'eyrir', 'undue', 'stagy', 'slimy',
         'sooty', 'batty', 'whore', 'raise', 'vetch', 'rhyme', 'wreak', 'cheap', 'needy', 'mossy', 'picky', 'bowed',
         'matte', 'serif', 'vital', 'ruler', 'divan', 'reedy', 'wahoo', 'perch', 'alter', 'dacha', 'sleet', 'obese',
         'brawn', 'baric', 'conto', 'flory', 'along', 'bairn', 'foamy', 'arena', 'lingo', 'sedan', 'halal', 'movie',
         'shawl', 'hovel', 'loins', 'cameo', 'crave', 'hyena', 'quine', 'urban', 'stick', 'nihil', 'jello', 'wales',
         'yeast', 'catty', 'fudge', 'adorn', 'caper', 'dally', 'licit', 'owlet', 'scend', 'letup', 'sprog', 'savvy',
         'steps', 'hacek', 'fetid', 'swish', 'octal', 'gecko', 'radio', 'mogul', 'lunch', 'think', 'edged', 'tinge',
         'swami', 'matey', 'trave', 'times', 'owner', 'radon', 'scurf', 'eclat', 'purse', 'beach', 'manta', 'brick',
         'bused', 'indie', 'smite', 'bowse', 'blade', 'tanka', 'would', 'algid', 'weird', 'stand', 'rushy', 'irons',
         'wrist', 'shack', 'dated', 'humus', 'newer', 'ionic', 'beery', 'cobra', 'intro', 'hakim', 'lacer', 'quote',
         'state', 'cower', 'sahib', 'ratel', 'dimly', 'preen', 'grits', 'gaily', 'dying', 'undid', 'vouge', 'murre',
         'mousy', 'crazy', 'roost', 'pupal', 'ovolo', 'umber', 'bitty', 'throw', 'score', 'notch', 'antic', 'pause',
         'sperm', 'shift', 'barye', 'lobby', 'chino', 'panel', 'tuner', 'inert', 'tesla', 'patch', 'axiom', 'lathi',
         'print', 'dazed', 'cedar', 'burnt', 'mamba', 'wince', 'poker', 'freer', 'elemi', 'slung', 'paste', 'spark',
         'forgo', 'wanly', 'pious', 'clout', 'sworn', 'value', 'laver', 'imbue', 'touch', 'demur', 'roper', 'booze',
         'chant', 'horst', 'bandy', 'sense', 'macro', 'aloof', 'piney', 'humid', 'gutsy', 'tibia', 'forty', 'icily',
         'larva', 'olden', 'miner', 'laity', 'offer', 'crimp', 'bitch', 'fetch', 'sauna', 'spend', 'graft', 'serer',
         'woozy', 'deter', 'blown', 'cabal', 'wrong', 'juice', 'daily', 'range', 'cured', 'minty', 'rotor', 'oasis',
         'query', 'anise', 'salty', 'lager', 'slurp', 'quick', 'cycle', 'grosz', 'tarot', 'spook', 'armed', 'quern',
         'funny', 'wound', 'ceric', 'scrod', 'sonar', 'width', 'acrid', 'puree', 'kopje', 'trout', 'corse', 'creak',
         'golem', 'sloop', 'smock', 'swamp', 'grain', 'vying', 'baize', 'bleat', 'volva', 'topic', 'ankus', 'goral',
         'alpha', 'lupus', 'peach', 'tipsy', 'donne', 'coach', 'agave', 'exude', 'gland', 'rabbi', 'agama', 'misty',
         'hanks', 'build', 'aroma', 'therm', 'curia', 'patty', 'small', 'chirk', 'usual', 'snide', 'cheer', 'parch',
         'refit', 'lower', 'taboo', 'novel', 'lover', 'south', 'sibyl', 'scrag', 'fumed', 'skiff', 'byway', 'motel',
         'pasta', 'fraud', 'words', 'sleep', 'scowl', 'anvil', 'ngwee', 'screw', 'sheer', 'erupt', 'frill', 'gluon',
         'gnarl', 'fiery', 'shied', 'skirt', 'wider', 'plank', 'unfit', 'court', 'rerun', 'liken', 'theca', 'brine',
         'taxis', 'vegan', 'baked', 'class', 'funds', 'kraut', 'merit', 'basal', 'broad', 'merge', 'demon', 'quite',
         'bimbo', 'hydra', 'pitch', 'conga', 'turbo', 'caput', 'hyson', 'sushi', 'stamp', 'grunt', 'cough', 'mater',
         'globe', 'vexed', 'itchy', 'kylix', 'solid', 'sedum', 'aggro', 'spawn', 'sized', 'leave', 'array', 'plunk',
         'rates', 'cycad', 'feast', 'gulch', 'adopt', 'bosom', 'kneel', 'trier', 'aerie', 'twill', 'speck', 'stoop',
         'lined', 'foist', 'nomad', 'tramp', 'souse', 'rowan', 'torte', 'tilde', 'press', 'blind', 'beady', 'legal',
         'cruet', 'durum', 'fishy', 'avoid', 'ditto', 'batik', 'paint', 'platy', 'hunch', 'bumpy', 'retch', 'shelf',
         'varus', 'piety', 'creme', 'ghost', 'reign', 'astir', 'conch', 'staff', 'ledge', 'cluck', 'fifth', 'atone',
         'tacit', 'baker', 'sheik', 'chink', 'toner', 'ramen', 'plied', 'guava', 'nohow', 'hotel', 'oiled', 'beard',
         'rumen', 'bylaw', 'balsa', 'folly', 'ponce', 'blimp', 'awash', 'abies', 'tribe', 'glint', 'flash', 'lilac',
         'dance', 'gimel', 'kebab', 'wrest', 'toast', 'scorn', 'lungi', 'dowdy', 'manic', 'crone', 'scamp', 'vesta',
         'large', 'fatwa', 'sutra', 'craze', 'talon', 'stria', 'kroon', 'clank', 'edify', 'study', 'siren', 'frore',
         'froze', 'vaunt', 'elder', 'peony', 'witty', 'foyer', 'sever', 'unbar', 'heart', 'mucky', 'beryl', 'jewel',
         'edger', 'kinin', 'trill', 'buggy', 'tutor', 'keyed', 'cline', 'gyral', 'mesic', 'block', 'ultra', 'sepia',
         'newel', 'sills', 'shank', 'hazel', 'shook', 'climb', 'dough', 'pinna', 'sidle', 'scrub', 'stent', 'scare',
         'witch', 'ruder', 'today', 'redux', 'dhole', 'goofy', 'bevel', 'saver', 'tonga', 'flood', 'alike', 'erect',
         'rigid', 'sexed', 'expel', 'crowd', 'brant', 'coney', 'grope', 'jaded', 'lithe', 'utile', 'power', 'quoth',
         'begin', 'finch', 'sisal', 'heron', 'rebus', 'revel', 'quoit', 'dumpy', 'threw', 'chess', 'blaze', 'decal',
         'enjoy', 'grade', 'skate', 'taker', 'joust', 'reeve', 'cheep', 'ascot', 'dumps', 'largo', 'haulm', 'shear',
         'child', 'whale', 'flock', 'happy', 'probe', 'polls', 'haven', 'stark', 'frown', 'nudge', 'lumpy', 'aloud',
         'ingot', 'germy', 'thing', 'shave', 'shyly', 'adage', 'royal', 'raspy', 'tally', 'stipe', 'whose', 'lento',
         'trite', 'enact', 'craft', 'bogus', 'easel', 'opine', 'shale', 'churn', 'whoop', 'chain', 'idyll', 'jinks',
         'singe', 'knave', 'count', 'maker', 'speed', 'petal', 'pique', 'doily', 'shock', 'wrack', 'pupil', 'unwed',
         'learn', 'aorta', 'surly', 'found', 'apply', 'awoke', 'aloft', 'fling', 'fjord', 'joint', 'boule', 'diode',
         'field', 'wrath', 'agate', 'elves', 'shirt', 'rehab', 'apron', 'lunar', 'endow', 'japan', 'hosta', 'savoy',
         'g-man', 'admit', 'boffo', 'rowel', 'lough', 'vomer', 'punch', 'repel', 'lousy', 'brisk', 'filer', 'login',
         'rangy', 'eider', 'loupe', 'gleet', 'maxim', 'schwa', 'lewis', 'swale', 'strew', 'altar', 'lyric', 'ladle',
         'gnash', 'scent', 'toxic', 'myrrh', 'boron', 'gorge', 'plush', 'aster', 'boggy', 'skive', 'furan', 'aware',
         'darts', 'tokay', 'actin', 'sneer', 'refer', 'prior', 'chaff', 'tatty', 'bonus', 'brook', 'towel', 'dishy',
         'wooer', 'recto', 'bunco', 'froth', 'misdo', 'mouse', 'inure', 'curie', 'twine', 'ogler', 'cruse', 'flirt',
         'rubel', 'rally', 'emend', 'kapok', 'divvy', 'wheel', 'email', 'iliac', 'aired', 'atlas', 'bifid', 'doubt',
         'torus', 'ruddy', 'swarm', 'kelly', 'blues', 'nymph', 'fuzzy', 'sandy', 'trews', 'mummy', 'kudzu', 'sissy',
         'stirk', 'poise', 'burns', 'pinky', 'amide', 'heath', 'spica', 'essay', 'worst', 'pygmy', 'fuggy', 'dross',
         'besot', 'rearm', 'curvy', 'loath', 'relic', 'butty', 'quack', 'angry', 'forge', 'gnome', 'stile', 'crown',
         'diner', 'awful', 'dwarf', 'gyrus', 'pulpy', 'gooey', 'boson', 'rover', 'toddy', 'marry', 'weald', 'thane',
         'shame', 'stank', 'liege', 'pewee', 'tours', 'lodge', 'lurid', 'surge', 'speak', 'dully', 'moray', 'agony',
         'swine', 'truck', 'foray', 'skill', 'sappy', 'album', 'floor', 'soggy', 'nerdy', 'smear', 'table', 'splay',
         'bobby', 'coypu', 'stone', 'gauze', 'shaft', 'gluey', 'blase', 'aspen', 'alibi', 'hymen', 'gamut', 'candy',
         'grove', 'algal', 'rouge', 'basis', 'bagel', 'plump', 'owing', 'scoff', 'pukka', 'yacht', 'chine', 'bijou',
         'nimby', 'adept', 'spine', 'sully', 'pylon', 'glaze', 'crest', 'ninon', 'fermi', 'until', 'stunk', 'silks',
         'swath', 'wings', 'punks', 'alula', 'tight', 'queen', 'annoy', 'elide', 'weber', 'crude', 'booty', 'sitar',
         'shone', 'hobby', 'claim', 'extra', 'maybe', 'spurn', 'guest', 'epoxy', 'canty', 'sabre', 'satyr', 'farce',
         'chill', 'gawky', 'chord', 'phial', 'macho', 'fluke', 'suite', 'organ', 'micro', 'homer', 'deign', 'twang',
         'waltz', 'abhor', 'cumin', 'scrap', 'latte', 'canna', 'slink', 'reset', 'fusee', 'quota', 'hardy', 'shred',
         'glume', 'panto', 'taste', 'geode', 'plier', 'polyp', 'parse', 'lurch', 'soapy', 'whisk', 'untie', 'facer',
         'there', 'aging', 'icing', 'boozy', 'coyly', 'elver', 'genie', 'whiff', 'store', 'grume', 'quest', 'prong',
         'joist', 'chasm', 'gayer', 'knock', 'saved', 'truss', 'mazer', 'islet', 'tawny', 'cater', 'liked', 'exult',
         'kurus', 'attic', 'tidal', 'grape', 'orate', 'karat', 'brill', 'cimex', 'spore', 'horny', 'gloom', 'cubit',
         'x-ray', 'penis', 'vowel', 'vault', 'paper', 'gamer', 'slain', 'cacti', 'resin', 'linen', 'tench', 'cocoa',
         'amass', 'salve', 'olive', 'addax', 'sorry', 'proud', 'azote', 'noise', 'belch', 'elect', 'ascus', 'chert',
         'troop', 'stoma', 'leggy', 'moire', 'apple', 'cross', 'scale', 'odium', 'extol', 'jetty', 'gumma', 'prion',
         'navel', 'molal', 'polar', 'cords', 'sound', 'vinyl', 'sleek', 'trend', 'mimic', 'crank', 'carat', 'felon',
         'gassy', 'layer', 'scuff', 'whelp', 'manga', 'melee', 'dhoti', 'ardeb', 'venom', 'boned', 'hyrax', 'stuck',
         'culex', 'frump', 'eagle', 'onset', 'amity', 'chose', 'minim', 'fussy', 'scrip', 'model', 'acned', 'forth',
         'tread', 'booth', 'thyme', 'badly', 'groin', 'broth', 'stern', 'slops', 'verso', 'bream', 'crick', 'cease',
         'piste', 'steer', 'lysin', 'guilt', 'hippy', 'spree', 'haiku', 'rower', 'filar', 'co-ed', 'chomp', 'kenaf',
         'fiend', 'whish', 'crook', 'ovine', 'seamy', 'parka', 'waxen', 'umbra', 'dwell', 'halon', 'lindy', 'flaky',
         'snare', 'rural', 'billy', 'spike', 'sonic', 'lemon', 'slant', 'saucy', 'lorry', 'chute', 'loyal', 'truth',
         'stuff', 'apian', 'enter', 'ivory', 'wring', 'vouch', 'nancy', 'curve', 'squat', 'beefy', 'lethe', 'farad',
         'jazzy', 'leach', 'marsh', 'sedge', 'loose', 'hitch', 'radii', 'beech', 'fizzy', 'nippy', 'beads', 'tacky',
         'blank', 'shirk', 'gully', 'vanda', 'grand', 'ditch', 'testa', 'crash', 'spang', 'alert', 'mined', 'eerie',
         'genus', 'karma', 'moped', 'beget', 'eject', 'feign', 'proxy', 'berry', 'nacho', 'scute', 'shrew', 'wrung',
         'snarl', 'hammy', 'stump', 'troat', 'slunk', 'inner', 'papal', 'stack', 'brash', 'hogan', 'stage', 'blain',
         'saner', 'shrug', 'start', 'fruit', 'dosed', 'milky', 'alder', 'showy', 'fried', 'least', 'spear', 'mango',
         'dowel', 'adder', 'oaten', 'belay', 'lasso', 'world', 'reify', 'bluer', 'creek', 'sport', 'maple', 'teeth',
         'abort', 'cocos', 'clang', 'kabob', 'unsex', 'empty', 'stoke', 'yokel', 'space', 'brake', 'blitz', 'angel',
         'dowse', 'irony', 'timid', 'china', 'sente', 'bench', 'madam', 'bound', 'amuck', 'glued', 'click', 'shall',
         'tryst', 'quiet', 'moron', 'petty', 'twirl', 'light', 'duvet', 'fetal', 'amaze', 'tough', 'serum', 'dozen',
         'cried', 'rinse', 'decry', 'abyss', 'matzo', 'loser', 'unzip', 'forte', 'round', 'liana', 'sinew', 'rondo',
         'elude', 'amine', 'paddy', 'emery', 'aglet', 'uvula', 'trial', 'gates', 'shawm', 'kasha', 'armet', 'shark',
         'whole', 'mills', 'stake', 'minus', 'stein', 'shard', 'chump', 'azoic', 'infix', 'vista', 'clasp', 'dried',
         'ulema', 'abode', 'cause', 'flier', 'harsh', 'khoum', 'lifer', 'tongs', 'pasty', 'droit', 'brier', 'joule',
         'awned', 'gazer', 'sedgy', 'snout', 'digit', 'jumbo', 'motif', 'stole', 'biome', 'drool', 'scour', 'daunt',
         'clerk', 'smell', 'broil', 'vogue', 'mover', 'could', 'outgo', 'epoch', 'larch', 'civet', 'loach', 'torah',
         'scald', 'aioli', 'ocean', 'amber', 'howdy', 'sieve', 'balmy', 'credo', 'elfin', 'costs', 'alien', 'mushy',
         'taken', 'socle', 'dodge', 'gruff', 'prawn', 'ready', 'pilaf', 'crypt', 'arise', 'thump', 'ninny', 'banks',
         'occur', 'delve', 'devil', 'thuja', 'cairn', 'meson', 'mount', 'canal', 'renal', 'vague', 'swirl', 'moved',
         'clued', 'eidos', 'prank', 'takin', 'lemur', 'laced', 'brute', 'align', 'saran', 'strut', 'allay', 'often',
         'fully', 'brink', 'chock', 'snips', 'agree', 'dixie', 'morph', 'pesto', 'glans', 'scull', 'canon', 'stoup',
         'xylem', 'agile', 'emcee', 'infer', 'float', 'skein', 'lemma', 'swash', 'brood', 'eager', 'tease', 'pearl',
         'ovary', 'amigo', 'quirk', 'crock', 'ahead', 'ninth']


def wordle_round(existing, correct_position, nope, words, not_in_correct_position):
    if len(list(set(existing))) != len(existing):
        def filter_existing_spe(x):
            for i in existing:
                if existing.count(i) > 1:
                    if x.count(i) < existing.count(i):
                        return False
                else:
                    if i not in x:
                        return False
            return True

        words = list(filter(filter_existing_spe, words))


    else:
        def filter_existing(x):
            for i in existing:
                if i not in x:
                    return False
            return True

        words = list(filter(filter_existing, words))

    for i in nope:
        if i in existing or i in correct_position:
            nope.remove(i)

    def filter_does_not_exist(x):
        for i in nope:
            if i in x:
                return False
        return True

    words = list(filter(filter_does_not_exist, words))

    def change_list(x):
        if x == '-':
            return ''
        else:
            return x

    correct_position = list(map(change_list, correct_position))

    def filter_correct_pos(x):
        if any(correct_position):
            for index, i in enumerate(correct_position):
                if i:
                    if x[index] != i:
                        return False
        return True

    words = list(filter(filter_correct_pos, words))

    def filter_wrong_pos(x):
        for index, a in enumerate(not_in_correct_position):
            for wrong_letter in a:
                if x[index] == wrong_letter:
                    return False
        return True

    words = list(filter(filter_wrong_pos, words))

    if words:
        return words[0], existing, correct_position, nope, words


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://wordlegame.org//")
    time.sleep(4)
    words = ['north', 'roach', 'spoof', 'areal', 'solar', 'bogey', 'gamey', 'affix', 'levee', 'bride', 'beret', 'ripen',
             'exile', 'usher', 'falls', 'trope', 'pieta', 'atoll', 'mirth', 'birth', 'pluck', 'caber', 'sling', 'allot',
             'amuse', 'belle', 'torch', 'wench', 'melon', 'tenor', 'roger', 'gauss', 'abohm', 'maund', 'razor', 'verst',
             'flick', 'frisk', 'bleep', 'jolly', 'bully', 'meaty', 'nerve', 'spoil', 'butte', 'swing', 'picul', 'greed',
             'clack', 'setup', 'posit', 'brail', 'noted', 'bible', 'nyala', 'munch', 'covey', 'saute', 'women', 'colic',
             'taunt', 'spunk', 'queue', 'shove', 'hasty', 'whirl', 'raver', 'taxer', 'yo-yo', 'crass', 'knell', 'brand',
             'madly', 'throe', 'dryer', 'oaken', 'swoon', 'bliss', 'sprue', 'gaunt', 'sabot', 'rowdy', 'apery', 'nadir',
             'voila', 'steam', 'fritz', 'aloes', 'white', 'might', 'cubby', 'decoy', 'assay', 'skink', 'apart', 'dolly',
             'envoy', 'alkyd', 'bathe', 'spool', 'whelk', 'pubis', 'gavel', 'naira', 'steak', 'lobar', 'carve', 'fable',
             'scrum', 'metro', 'areca', 'oldie', 'shape', 'plaid', 'steal', 'slide', 'abbot', 'havoc', 'shore', 'mural',
             'harem', 'churr', 'these', 'above', 'panic', 'droll', 'khaki', 'hewer', 'tempo', 'mufti', 'usury', 'charm',
             'rocky', 'pubic', 'tumid', 'grout', 'which', 'brave', 'radar', 'locus', 'vocal', 'apish', 'fauna', 'dicot',
             'fusty', 'noose', 'blini', 'calve', 'egret', 'latex', 'dodgy', 'tithe', 'hyper', 'focal', 'kraal', 'ichor',
             'bialy', 'sabra', 'odder', 'knead', 'mambo', 'laxly', 'verve', 'spiky', 'smuts', 'dregs', 'cliff', 'linin',
             'whack', 'prang', 'quasi', 'furry', 'silky', 'amiss', 'zloty', 'taint', 'trait', 'papaw', 'style', 'scram',
             'alive', 'spray', 'cling', 'glade', 'manes', 'dicer', 'messy', 'thumb', 'focus', 'jelly', 'bawdy', 'diver',
             'chick', 'bulla', 'debug', 'swore', 'false', 'corer', 'offal', 'haler', 'about', 'parer', 'brunt', 'scion',
             'meter', 'spell', 'privy', 'willy', 'ranch', 'mayor', 'boast', 'young', 'giddy', 'woody', 'ounce', 'sheet',
             'cheek', 'virus', 'batch', 'riper', 'fella', 'rough', 'butch', 'quoin', 'cense', 'salad', 'grass', 'imago',
             'fixer', 'mucor', 'smash', 'squaw', 'event', 'bloke', 'loamy', 'scene', 'femur', 'fleet', 'arson', 'dimer',
             'shirr', 'louis', 'boric', 'velar', 'amend', 'vivid', 'guard', 'dusty', 'derby', 'dress', 'murky', 'stock',
             'bleed', 'spare', 'rummy', 'patio', 'relax', 'bayou', 'meany', 'cadet', 'award', 'eying', 'deity', 'hinny',
             'tenon', 'rajah', 'syrup', 'ileum', 'blush', 'trove', 'acute', 'straw', 'donna', 'hoist', 'laser', 'vagus',
             'jimmy', 'swoop', 'loner', 'serow', 'drink', 'trace', 'suety', 'quark', 'bongo', 'emmer', 'buxom', 'hired',
             'shill', 'ratty', 'yenta', 'match', 'fossa', 'pinko', 'squab', 'peril', 'parts', 'evade', 'pipit', 'benny',
             'rupee', 'chyme', 'filet', 'whiny', 'drier', 'braze', 'codon', 'flats', 'spume', 'ovule', 'potty', 'cisco',
             'daisy', 'plead', 'surer', 'rival', 'thank', 'baron', 'snuff', 'niche', 'steel', 'rarer', 'truer', 'prone',
             'stood', 'vireo', 'thrum', 'cabin', 'umbel', 'sucre', 'mercy', 'tenge', 'copal', 'rodeo', 'rainy', 'flour',
             'toned', 'luffa', 'wimpy', 'sweat', 'chirr', 'issue', 'tooth', 'spite', 'musty', 'tempt', 'tenet', 'auxin',
             'sight', 'theme', 'peter', 'comet', 'virga', 'musky', 'missy', 'breed', 'cubeb', 'tasty', 'befit', 'tinea',
             'terce', 'aping', 'feria', 'gravy', 'frizz', 'hoard', 'cutin', 'clamp', 'sweep', 'molar', 'chair', 'blunt',
             'going', 'stomp', 'antsy', 'aloha', 'deist', 'nanny', 'softy', 'pizza', 'bloat', 'guyot', 'sylph', 'pitta',
             'fauve', 'worse', 'gaffe', 'annul', 'kopek', 'leone', 'again', 'sadhu', 'among', 'elite', 'opera', 'betel',
             'drunk', 'hooks', 'tuber', 'drone', 'sheen', 'idler', 'jenny', 'grebe', 'chufa', 'share', 'guise', 'dingy',
             'third', 'oread', 'mound', 'peaky', 'still', 'toque', 'seedy', 'inion', 'niece', 'gesso', 'troll', 'carry',
             'snook', 'spiff', 'leafy', 'crore', 'mongo', 'bored', 'droop', 'pouch', 'flint', 'thong', 'ample', 'craps',
             'ebony', 'wafer', 'fusil', 'shire', 'sower', 'xerox', 'black', 'caulk', 'alias', 'kappa', 'prick', 'raven',
             'lucky', 'titan', 'mourn', 'incur', 'ashen', 'built', 'stork', 'pence', 'carom', 'human', 'cutch', 'midge',
             'check', 'spoor', 't-man', 'taffy', 'wryly', 'sugar', 'raper', 'junta', 'twerp', 'fatso', 'filmy', 'nervy',
             'psalm', 'breve', 'aural', 'geese', 'mated', 'kafir', 'shrub', 'baggy', 'hilum', 'aroid', 'spicy', 'manat',
             'known', 'buyer', 'stink', 'magus', 'arose', 'fovea', 'ensue', 'dogma', 'tenth', 'thebe', 'grave', 'monad',
             'sweet', 'tubed', 'corps', 'wield', 'hussy', 'march', 'sigma', 'spank', 'hippo', 'ravel', 'dopey', 'scree',
             'robot', 'other', 'swept', 'hooch', 'quake', 'squad', 'flare', 'annex', 'champ', 'briny', 'baler', 'bursa',
             'leaky', 'prude', 'quart', 'board', 'level', 'equal', 'abuzz', 'baton', 'moody', 'rabid', 'poppy', 'dulse',
             'horde', 'bruin', 'kitty', 'piper', 'trail', 'segno', 'bolus', 'sixth', 'seven', 'twist', 'louse', 'cloud',
             'igloo', 'cecum', 'amain', 'winch', 'diazo', 'urial', 'tabby', 'soled', 'mauve', 'manky', 'dunce', 'knack',
             'metal', 'liger', 'pilot', 'links', 'scape', 'atilt', 'storm', 'vigil', 'tower', 'quiff', 'perry', 'naris',
             'ember', 'lapse', 'posed', 'thunk', 'lunge', 'ridge', 'weedy', 'udder', 'whine', 'domed', 'eater', 'groan',
             'vagal', 'grime', 'agent', 'bingo', 'solan', 'pried', 'croft', 'hater', 'giver', 'jumpy', 'stint', 'blame',
             'alley', 'cozen', 'wacky', 'algin', 'swung', 'exert', 'allow', 'inane', 'nexus', 'allyl', 'friar', 'durra',
             'audio', 'wedge', 'dingo', 'limey', 'early', 'phyle', 'servo', 'crust', 'unity', 'artsy', 'riser', 'medal',
             'finer', 'fleer', 'covet', 'spout', 'proof', 'track', 'clump', 'manna', 'baste', 'shaky', 'lefty', 'draft',
             'comma', 'entry', 'kayak', 'flack', 'warty', 'teary', 'queer', 'waist', 'heavy', 'mothy', 'gonad', 'snail',
             'telex', 'suing', 'thief', 'terse', 'joker', 'bosky', 'teens', 'clear', 'risen', 'medic', 'henry', 'fakir',
             'ditty', 'dicky', 'testy', 'tonic', 'genre', 'swage', 'macaw', 'frank', 'nylon', 'slate', 'halve', 'water',
             'sprig', 'helix', 'lapin', 'newsy', 'drake', 'obeah', 'gouge', 'stout', 'clone', 'evoke', 'thigh', 'dolce',
             'hedge', 'smoke', 'boxer', 'leper', 'elate', 'great', 'slack', 'twixt', 'avail', 'puffy', 'crane', 'stoat',
             'bones', 'babel', 'coven', 'comfy', 'salvo', 'unmet', 'order', 'negus', 'aptly', 'scuba', 'baiza', 'nosed',
             'enemy', 'roble', 'shade', 'vapid', 'ought', 'oakum', 'unset', 'filth', 'fight', 'snowy', 'silly', 'fence',
             'token', 'hajji', 'slush', 'unite', 'fresh', 'siege', 'debit', 'faced', 'chime', 'asper', 'gloat', 'liner',
             'hawse', 'squib', 'borne', 'geeky', 'naked', 'aider', 'fugal', 'gleam', 'coati', 'nawab', 'fault', 'bicep',
             'tulle', 'imply', 'rouse', 'bland', 'sinus', 'modem', 'logic', 'ninja', 'river', 'bedew', 'mafia', 'twins',
             'mucus', 'abuse', 'flies', 'dread', 'cauda', 'cavil', 'silva', 'lipid', 'cynic', 'slime', 'silty', 'cleat',
             'magic', 'scope', 'facet', 'dwelt', 'paean', 'union', 'brawl', 'aback', 'snaky', 'blink', 'pasha', 'aspic',
             'optic', 'prove', 'tiler', 'pacer', 'paisa', 'plait', 'solve', 'chard', 'argue', 'lathe', 'metis', 'racer',
             'gauge', 'youth', 'avian', 'pinto', 'vulva', 'posse', 'grant', 'snick', 'skirl', 'picot', 'ankle', 'snack',
             'renin', 'dinky', 'prate', 'habit', 'flung', 'rugby', 'dildo', 'lisle', 'decor', 'bally', 'midst', 'godly',
             'feint', 'jiffy', 'guide', 'grief', 'worry', 'unlit', 'drama', 'doped', 'burgh', 'swear', 'valid', 'snort',
             'limbo', 'bonny', 'equip', 'retry', 'torso', 'trunk', 'maria', 'usurp', 'psoas', 'basic', 'three', 'slope',
             'harpy', 'kneed', 'owned', 'poach', 'folio', 'wagon', 'spoke', 'acerb', 'sprit', 'otter', 'ideal', 'adapt',
             'lobed', 'biter', 'venue', 'parks', 'algae', 'revue', 'sable', 'moral', 'lumen', 'begat', 'salon', 'logan',
             'viper', 'pulse', 'glove', 'angle', 'monte', 'fives', 'arete', 'total', 'timed', 'davit', 'randy', 'sniff',
             'galea', 'vomit', 'croup', 'bight', 'guile', 'tayra', 'haste', 'incus', 'gypsy', 'klutz', 'manor', 'sunny',
             'gusty', 'dummy', 'acorn', 'etude', 'harry', 'chyle', 'prime', 'musth', 'gemma', 'irate', 'wager', 'price',
             'drift', 'plain', 'watch', 'viand', 'clung', 'recap', 'chaos', 'canoe', 'burst', 'cupid', 'limit', 'viral',
             'laden', 'cello', 'curio', 'blahs', 'video', 'reach', 'banns', 'recur', 'clown', 'gaudy', 'began', 'roads',
             'rheum', 'quell', 'leapt', 'borax', 'orbit', 'snood', 'realm', 'treat', 'ethyl', 'futon', 'anime', 'canto',
             'pudgy', 'flair', 'zaire', 'hover', 'bough', 'scary', 'heaps', 'grist', 'stave', 'zonal', 'mulch', 'piton',
             'sough', 'doing', 'sorus', 'runic', 'props', 'delay', 'phase', 'oddly', 'bugle', 'wreck', 'quill', 'pagan',
             'mangy', 'choke', 'juicy', 'deuce', 'douse', 'chide', 'blond', 'shake', 'darky', 'cocky', 'eland', 'fichu',
             'lotto', 'weepy', 'abbey', 'auger', 'aphid', 'mecca', 'franc', 'dusky', 'amino', 'latch', 'idiom', 'rumba',
             'smirk', 'cigar', 'place', 'cream', 'ethos', 'degas', 'oxide', 'sewed', 'evert', 'tying', 'using', 'zoril',
             'fatal', 'mason', 'loved', 'ester', 'inlay', 'sebum', 'clock', 'roast', 'break', 'hatch', 'liver', 'snore',
             'flail', 'pushy', 'crony', 'crime', 'knish', 'motet', 'detox', 'ketch', 'ivied', 'truly', 'creed', 'palsy',
             'await', 'flask', 'yield', 'whist', 'rivet', 'modal', 'colon', 'nobly', 'sixty', 'booby', 'pubes', 'flank',
             'route', 'doggo', 'cadre', 'seine', 'binge', 'write', 'ennui', 'motto', 'unman', 'usage', 'soupy', 'aedes',
             'dizzy', 'enema', 'tense', 'rifle', 'cornu', 'gammy', 'tiled', 'cabby', 'saint', 'rebel', 'steep', 'mania',
             'debar', 'phlox', 'rosin', 'burly', 'elbow', 'agape', 'carob', 'buteo', 'upend', 'bocce', 'meant', 'croon',
             'muser', 'remit', 'flesh', 'qibla', 'lance', 'swede', 'varix', 'glory', 'tabor', 'utter', 'welsh', 'numen',
             'bravo', 'bulky', 'bossy', 'splat', 'skier', 'avert', 'upper', 'worth', 'dilly', 'hypha', 'frost', 'curse',
             'terra', 'cargo', 'sadly', 'smelt', 'quits', 'trick', 'rebut', 'rogue', 'crawl', 'bison', 'broom', 'askew',
             'dealt', 'quaff', 'flown', 'femme', 'besom', 'kazoo', 'circa', 'hinge', 'dogie', 'conic', 'feral', 'clary',
             'pouty', 'synod', 'peaty', 'guppy', 'magma', 'ducat', 'peeve', 'graph', 'burin', 'knife', 'ovate', 'spiny',
             'caret', 'calyx', 'pixel', 'sepal', 'coast', 'basin', 'caste', 'lagan', 'lease', 'omega', 'major', 'milch',
             'honey', 'tabes', 'flume', 'fewer', 'theft', 'manse', 'drill', 'gross', 'no-go', 'fanny', 'civil', 'stoic',
             'super', 'gloss', 'drove', 'mealy', 'train', 'lotus', 'oxbow', 'house', 'paved', 'tepid', 'gofer', 'lapel',
             'xeric', 'spitz', 'teddy', 'butut', 'niffy', 'virtu', 'anger', 'final', 'renew', 'edict', 'smart', 'copra',
             'defer', 'foggy', 'dower', 'tinny', 'hurry', 'shown', 'clove', 'short', 'react', 'flunk', 'firth', 'tract',
             'urine', 'penal', 'newly', 'leery', 'disco', 'adult', 'brown', 'grown', 'alate', 'coact', 'fatty', 'elegy',
             'stool', 'spade', 'withe', 'graze', 'kanzu', 'afire', 'valet', 'strip', 'wally', 'carol', 'chafe', 'stray',
             'debut', 'prize', 'verge', 'chalk', 'cuddy', 'cramp', 'parry', 'tardy', 'inkle', 'sassy', 'pogge', 'pride',
             'couch', 'wages', 'squid', 'smile', 'vedic', 'brief', 'qualm', 'since', 'steed', 'lying', 'natal', 'piece',
             'haply', 'yodel', 'cinch', 'stunt', 'quail', 'shalt', 'viola', 'retie', 'couth', 'night', 'fifty', 'creep',
             'noble', 'hertz', 'pleat', 'month', 'yearn', 'middy', 'goody', 'recce', 'burke', 'serge', 'slang', 'beige',
             'maser', 'cuppa', 'crate', 'blurt', 'libel', 'tamed', 'namer', 'outdo', 'canny', 'henna', 'mudra', 'teach',
             'windy', 'tripe', 'ology', 'tweed', 'frame', 'fetus', 'crape', 'anile', 'terry', 'delft', 'blend', 'drank',
             'means', 'resew', 'wordy', 'potto', 'whizz', 'lever', 'voter', 'exact', 'villa', 'mucin', 'loopy', 'goose',
             'wheat', 'bribe', 'anima', 'erase', 'slick', 'bowel', 'neigh', 'spent', 'peace', 'bhang', 'copse', 'stare',
             'ukase', 'under', 'shine', 'plant', 'fairy', 'ploce', 'cacao', 'quipu', 'fiver', 'weary', 'verse', 'cache',
             'gouty', 'reuse', 'earth', 'theta', 'semen', 'thick', 'purer', 'anion', 'tarry', 'aglow', 'slave', 'swank',
             'wispy', 'ether', 'wirer', 'coupe', 'rhino', 'argon', 'koala', 'shady', 'noisy', 'risky', 'clink', 'naiad',
             'ohmic', 'jabot', 'knoll', 'unfed', 'tangy', 'relay', 'snake', 'costa', 'upset', 'first', 'grasp', 'creel',
             'sneak', 'divot', 'balas', 'pinon', 'shunt', 'lysis', 'uncle', 'inset', 'admin', 'belly', 'eared', 'knelt',
             'works', 'salsa', 'gumbo', 'aisle', 'inept', 'bread', 'bezel', 'title', 'dense', 'mooch', 'choir', 'abase',
             'cloth', 'green', 'sumac', 'grail', 'okapi', 'brain', 'libra', 'ficus', 'crepe', 'waive', 'throb', 'crack',
             'sabin', 'hound', 'scaly', 'mouth', 'greet', 'clews', 'sewer', 'puppy', 'guild', 'genic', 'shiny', 'comic',
             'alone', 'trump', 'plumb', 'mower', 'strap', 'flute', 'totem', 'spoon', 'ergot', 'botch', 'calla', 'zesty',
             'oiler', 'stilt', 'mamey', 'freak', 'zayin', 'amble', 'where', 'agora', 'skunk', 'putty', 'dowry', 'plonk',
             'wired', 'saiga', 'azure', 'indic', 'bunny', 'kauri', 'crake', 'frail', 'sorgo', 'wiser', 'sword', 'lexis',
             'valve', 'codex', 'swipe', 'slump', 'jaunt', 'golly', 'bring', 'trash', 'porgy', 'bract', 'd-day', 'flora',
             'sooth', 'music', 'onion', 'girly', 'mumps', 'bloom', 'jorum', 'boxed', 'drupe', 'stogy', 'admix', 'older',
             'adust', 'begum', 'cress', 'vicar', 'curry', 'flame', 'imide', 'poesy', 'recut', 'spied', 'penny', 'faint',
             'abaca', 'force', 'fluff', 'mulct', 'adobe', 'blood', 'octet', 'ulcer', 'eight', 'voice', 'leech', 'split',
             'prowl', 'croak', 'rusty', 'hefty', 'miler', 'piggy', 'manly', 'chore', 'denim', 'nasal', 'beamy', 'handy',
             'safer', 'ceiba', 'aalii', 'story', 'barge', 'stung', 'whomp', 'drain', 'grimy', 'hello', 'boost', 'sheep',
             'deism', 'stiff', 'holly', 'skulk', 'genet', 'abate', 'tansy', 'ghoul', 'party', 'scarf', 'nutty', 'gusto',
             'prism', 'avens', 'piano', 'enate', 'arced', 'adore', 'payer', 'watts', 'decay', 'swell', 'sprag', 'glide',
             'morse', 'glass', 'thill', 'cobia', 'aldol', 'close', 'slash', 'fixed', 'zamia', 'julep', 'educe', 'exist',
             'pansy', 'overt', 'shiva', 'flump', 'inlet', 'shell', 'scoop', 'cover', 'dutch', 'basil', 'tulip', 'flush',
             'esker', 'voile', 'death', 'flake', 'topaz', 'coral', 'banal', 'butyl', 'suave', 'group', 'porch', 'jural',
             'bless', 'snipe', 'snafu', 'ephah', 'elope', 'ruled', 'gummy', 'catch', 'daddy', 'oriel', 'morel', 'ritzy',
             'pooch', 'johns', 'dryly', 'bigot', 'nicer', 'dinge', 'sprat', 'lanai', 'frond', 'trade', 'hyoid', 'stale',
             'nones', 'serve', 'visor', 'begun', 'unify', 'phone', 'hijab', 'argil', 'druid', 'skeet', 'dairy', 'freed',
             'pommy', 'junco', 'dandy', 'claro', 'rapid', 'osier', 'dobra', 'plume', 'hydro', 'lowly', 'snoop', 'their',
             'budge', 'flout', 'outer', 'mince', 'spire', 'bushy', 'bovid', 'purge', 'fever', 'given', 'elute', 'drawn',
             'nidus', 'chewy', 'mixer', 'azide', 'penni', 'cleft', 'gripe', 'stalk', 'trawl', 'muggy', 'adieu', 'waxed',
             'stall', 'pedal', 'salmi', 'later', 'drawl', 'belie', 'cable', 'giant', 'tapir', 'cutie', 'prink', 'sulky',
             'roomy', 'aleph', 'lofty', 'xenon', 'broke', 'bacon', 'gamma', 'plaza', 'vodka', 'fucus', 'hexed', 'right',
             'ricer', 'satin', 'weave', 'bated', 'chuck', 'rayon', 'shout', 'those', 'talus', 'tubal', 'genip', 'widow',
             'pavis', 'sober', 'badge', 'berth', 'merry', 'braid', 'stash', 'banjo', 'wells', 'pecan', 'noria', 'timer',
             'jerky', 'horse', 'ulnar', 'gruel', 'cased', 'motor', 'fluid', 'trice', 'moist', 'after', 'alarm', 'regal',
             'tonal', 'minor', 'actor', 'emote', 'grate', 'nasty', 'miser', 'forum', 'huffy', 'tamer', 'bidet', 'chest',
             'crumb', 'depth', 'kraft', 'drown', 'afoul', 'gonif', 'strop', 'visit', 'jihad', 'knout', 'stove', 'angst',
             'wiper', 'suede', 'slice', 'v-day', 'perky', 'datum', 'repay', 'shoal', 'litas', 'ilium', 'yucca', 'hunky',
             'slake', 'birch', 'judge', 'kiosk', 'fungi', 'cloak', 'chase', 'spurt', 'redly', 'below', 'scalp', 'dirty',
             'gable', 'goner', 'dream', 'spice', 'arrow', 'sting', 'cider', 'non-u', 'salol', 'zooid', 'quash', 'lotic',
             'senna', 'scant', 'dryad', 'condo', 'inbox', 'awake', 'afoot', 'patsy', 'being', 'uncut', 'laird', 'mores',
             'biota', 'biped', 'axial', 'crump', 'grace', 'smoky', 'local', 'biddy', 'spasm', 'stony', 'downy', 'depot',
             'burro', 'funky', 'dicey', 'truce', 'chief', 'romeo', 'gourd', 'clean', 'mamma', 'stain', 'beset', 'capon',
             'reply', 'toxin', 'tepee', 'tweet', 'growl', 'scrim', 'sloth', 'front', 'mammy', 'pivot', 'wharf', 'embed',
             'ethic', 'serin', 'waver', 'eking', 'input', 'yahoo', 'revet', 'bleak', 'wrote', 'spall', 'lusty', 'fugue',
             'abeam', 'taped', 'beast', 'hilly', 'tammy', 'hours', 'koine', 'hands', 'houri', 'brace', 'swill', 'poser',
             'marks', 'sauce', 'livid', 'attar', 'pyxie', 'tetra', 'shoot', 'crept', 'heady', 'cruel', 'tiger', 'inter',
             'waste', 'scout', 'impel', 'augur', 'krill', 'lymph', 'prune', 'faith', 'roots', 'corgi', 'ootid', 'unpin',
             'opium', 'prose', 'segue', 'kinky', 'lanky', 'grill', 'point', 'every', 'glare', 'based', 'comer', 'cubic',
             'humph', 'ducal', 'scold', 'tilth', 'smith', 'cecal', 'pithy', 'chela', 'llama', 'kvass', 'moose', 'alkyl',
             'folks', 'buddy', 'pesky', 'ozone', 'image', 'groom', 'vixen', 'tunic', 'nabob', 'krait', 'eaten', 'leash',
             'stupa', 'label', 'heave', 'woken', 'smack', 'samba', 'sharp', 'sally', 'drape', 'donor', 'nisei', 'alloy',
             'woven', 'bling', 'diary', 'plane', 'aside', 'asset', 'excel', 'metic', 'mange', 'fryer', 'guano', 'girth',
             'floss', 'weigh', 'polka', 'laugh', 'stair', 'erode', 'tired', 'dirge', 'weeds', 'amply', 'glyph', 'jawed',
             'glean', 'delta', 'seize', 'zebra', 'poilu', 'hairy', 'slept', 'crier', 'blare', 'cheat', 'grind', 'muddy',
             'brush', 'tiara', 'lucid', 'rider', 'ramie', 'curly', 'scone', 'woman', 'anode', 'tweak', 'brass', 'stead',
             'kiang', 'briar', 'quilt', 'audit', 'guess', 'nurse', 'drive', 'pixie', 'staid', 'heard', 'skimp', 'payee',
             'husky', 'paler', 'deify', 'gulag', 'frock', 'mocha', 'maize', 'thorn', 'gorse', 'juror', 'idiot', 'addle',
             'abide', 'rings', 'fancy', 'naval', 'haunt', 'evict', 'robin', 'skull', 'bluff', 'error', 'chirp', 'cushy',
             'naive', 'cagey', 'retro', 'hoary', 'llano', 'plate', 'hiker', 'civic', 'dekko', 'humic', 'duchy', 'spill',
             'filly', 'taper', 'swift', 'media', 'hutch', 'never', 'chunk', 'photo', 'clash', 'bulge', 'strum', 'roman',
             'camel', 'quirt', 'soave', 'ovoid', 'exalt', 'tried', 'pinch', 'blowy', 'primo', 'ratio', 'ferry', 'blurb',
             'oxime', 'money', 'vower', 'crisp', 'slosh', 'lynch', 'wight', 'bunch', 'bilge', 'aphis', 'triad', 'smote',
             'hotly', 'while', 'slyly', 'spiel', 'chart', 'senor', 'taupe', 'shush', 'genoa', 'pound', 'heist', 'blast',
             'jacks', 'trust', 'negro', 'twice', 'widen', 'tango', 'favus', 'holey', 'saury', 'corny', 'hence', 'crush',
             'marly', 'shuck', 'quire', 'eosin', 'loess', 'fleck', 'index', 'eaves', 'eyrir', 'undue', 'stagy', 'slimy',
             'sooty', 'batty', 'whore', 'raise', 'vetch', 'rhyme', 'wreak', 'cheap', 'needy', 'mossy', 'picky', 'bowed',
             'matte', 'serif', 'vital', 'ruler', 'divan', 'reedy', 'wahoo', 'perch', 'alter', 'dacha', 'sleet', 'obese',
             'brawn', 'baric', 'conto', 'flory', 'along', 'bairn', 'foamy', 'arena', 'lingo', 'sedan', 'halal', 'movie',
             'shawl', 'hovel', 'loins', 'cameo', 'crave', 'hyena', 'quine', 'urban', 'stick', 'nihil', 'jello', 'wales',
             'yeast', 'catty', 'fudge', 'adorn', 'caper', 'dally', 'licit', 'owlet', 'scend', 'letup', 'sprog', 'savvy',
             'steps', 'hacek', 'fetid', 'swish', 'octal', 'gecko', 'radio', 'mogul', 'lunch', 'think', 'edged', 'tinge',
             'swami', 'matey', 'trave', 'times', 'owner', 'radon', 'scurf', 'eclat', 'purse', 'beach', 'manta', 'brick',
             'bused', 'indie', 'smite', 'bowse', 'blade', 'tanka', 'would', 'algid', 'weird', 'stand', 'rushy', 'irons',
             'wrist', 'shack', 'dated', 'humus', 'newer', 'ionic', 'beery', 'cobra', 'intro', 'hakim', 'lacer', 'quote',
             'state', 'cower', 'sahib', 'ratel', 'dimly', 'preen', 'grits', 'gaily', 'dying', 'undid', 'vouge', 'murre',
             'mousy', 'crazy', 'roost', 'pupal', 'ovolo', 'umber', 'bitty', 'throw', 'score', 'notch', 'antic', 'pause',
             'sperm', 'shift', 'barye', 'lobby', 'chino', 'panel', 'tuner', 'inert', 'tesla', 'patch', 'axiom', 'lathi',
             'print', 'dazed', 'cedar', 'burnt', 'mamba', 'wince', 'poker', 'freer', 'elemi', 'slung', 'paste', 'spark',
             'forgo', 'wanly', 'pious', 'clout', 'sworn', 'value', 'laver', 'imbue', 'touch', 'demur', 'roper', 'booze',
             'chant', 'horst', 'bandy', 'sense', 'macro', 'aloof', 'piney', 'humid', 'gutsy', 'tibia', 'forty', 'icily',
             'larva', 'olden', 'miner', 'laity', 'offer', 'crimp', 'bitch', 'fetch', 'sauna', 'spend', 'graft', 'serer',
             'woozy', 'deter', 'blown', 'cabal', 'wrong', 'juice', 'daily', 'range', 'cured', 'minty', 'rotor', 'oasis',
             'query', 'anise', 'salty', 'lager', 'slurp', 'quick', 'cycle', 'grosz', 'tarot', 'spook', 'armed', 'quern',
             'funny', 'wound', 'ceric', 'scrod', 'sonar', 'width', 'acrid', 'puree', 'kopje', 'trout', 'corse', 'creak',
             'golem', 'sloop', 'smock', 'swamp', 'grain', 'vying', 'baize', 'bleat', 'volva', 'topic', 'ankus', 'goral',
             'alpha', 'lupus', 'peach', 'tipsy', 'donne', 'coach', 'agave', 'exude', 'gland', 'rabbi', 'agama', 'misty',
             'hanks', 'build', 'aroma', 'therm', 'curia', 'patty', 'small', 'chirk', 'usual', 'snide', 'cheer', 'parch',
             'refit', 'lower', 'taboo', 'novel', 'lover', 'south', 'sibyl', 'scrag', 'fumed', 'skiff', 'byway', 'motel',
             'pasta', 'fraud', 'words', 'sleep', 'scowl', 'anvil', 'ngwee', 'screw', 'sheer', 'erupt', 'frill', 'gluon',
             'gnarl', 'fiery', 'shied', 'skirt', 'wider', 'plank', 'unfit', 'court', 'rerun', 'liken', 'theca', 'brine',
             'taxis', 'vegan', 'baked', 'class', 'funds', 'kraut', 'merit', 'basal', 'broad', 'merge', 'demon', 'quite',
             'bimbo', 'hydra', 'pitch', 'conga', 'turbo', 'caput', 'hyson', 'sushi', 'stamp', 'grunt', 'cough', 'mater',
             'globe', 'vexed', 'itchy', 'kylix', 'solid', 'sedum', 'aggro', 'spawn', 'sized', 'leave', 'array', 'plunk',
             'rates', 'cycad', 'feast', 'gulch', 'adopt', 'bosom', 'kneel', 'trier', 'aerie', 'twill', 'speck', 'stoop',
             'lined', 'foist', 'nomad', 'tramp', 'souse', 'rowan', 'torte', 'tilde', 'press', 'blind', 'beady', 'legal',
             'cruet', 'durum', 'fishy', 'avoid', 'ditto', 'batik', 'paint', 'platy', 'hunch', 'bumpy', 'retch', 'shelf',
             'varus', 'piety', 'creme', 'ghost', 'reign', 'astir', 'conch', 'staff', 'ledge', 'cluck', 'fifth', 'atone',
             'tacit', 'baker', 'sheik', 'chink', 'toner', 'ramen', 'plied', 'guava', 'nohow', 'hotel', 'oiled', 'beard',
             'rumen', 'bylaw', 'balsa', 'folly', 'ponce', 'blimp', 'awash', 'abies', 'tribe', 'glint', 'flash', 'lilac',
             'dance', 'gimel', 'kebab', 'wrest', 'toast', 'scorn', 'lungi', 'dowdy', 'manic', 'crone', 'scamp', 'vesta',
             'large', 'fatwa', 'sutra', 'craze', 'talon', 'stria', 'kroon', 'clank', 'edify', 'study', 'siren', 'frore',
             'froze', 'vaunt', 'elder', 'peony', 'witty', 'foyer', 'sever', 'unbar', 'heart', 'mucky', 'beryl', 'jewel',
             'edger', 'kinin', 'trill', 'buggy', 'tutor', 'keyed', 'cline', 'gyral', 'mesic', 'block', 'ultra', 'sepia',
             'newel', 'sills', 'shank', 'hazel', 'shook', 'climb', 'dough', 'pinna', 'sidle', 'scrub', 'stent', 'scare',
             'witch', 'ruder', 'today', 'redux', 'dhole', 'goofy', 'bevel', 'saver', 'tonga', 'flood', 'alike', 'erect',
             'rigid', 'sexed', 'expel', 'crowd', 'brant', 'coney', 'grope', 'jaded', 'lithe', 'utile', 'power', 'quoth',
             'begin', 'finch', 'sisal', 'heron', 'rebus', 'revel', 'quoit', 'dumpy', 'threw', 'chess', 'blaze', 'decal',
             'enjoy', 'grade', 'skate', 'taker', 'joust', 'reeve', 'cheep', 'ascot', 'dumps', 'largo', 'haulm', 'shear',
             'child', 'whale', 'flock', 'happy', 'probe', 'polls', 'haven', 'stark', 'frown', 'nudge', 'lumpy', 'aloud',
             'ingot', 'germy', 'thing', 'shave', 'shyly', 'adage', 'royal', 'raspy', 'tally', 'stipe', 'whose', 'lento',
             'trite', 'enact', 'craft', 'bogus', 'easel', 'opine', 'shale', 'churn', 'whoop', 'chain', 'idyll', 'jinks',
             'singe', 'knave', 'count', 'maker', 'speed', 'petal', 'pique', 'doily', 'shock', 'wrack', 'pupil', 'unwed',
             'learn', 'aorta', 'surly', 'found', 'apply', 'awoke', 'aloft', 'fling', 'fjord', 'joint', 'boule', 'diode',
             'field', 'wrath', 'agate', 'elves', 'shirt', 'rehab', 'apron', 'lunar', 'endow', 'japan', 'hosta', 'savoy',
             'g-man', 'admit', 'boffo', 'rowel', 'lough', 'vomer', 'punch', 'repel', 'lousy', 'brisk', 'filer', 'login',
             'rangy', 'eider', 'loupe', 'gleet', 'maxim', 'schwa', 'lewis', 'swale', 'strew', 'altar', 'lyric', 'ladle',
             'gnash', 'scent', 'toxic', 'myrrh', 'boron', 'gorge', 'plush', 'aster', 'boggy', 'skive', 'furan', 'aware',
             'darts', 'tokay', 'actin', 'sneer', 'refer', 'prior', 'chaff', 'tatty', 'bonus', 'brook', 'towel', 'dishy',
             'wooer', 'recto', 'bunco', 'froth', 'misdo', 'mouse', 'inure', 'curie', 'twine', 'ogler', 'cruse', 'flirt',
             'rubel', 'rally', 'emend', 'kapok', 'divvy', 'wheel', 'email', 'iliac', 'aired', 'atlas', 'bifid', 'doubt',
             'torus', 'ruddy', 'swarm', 'kelly', 'blues', 'nymph', 'fuzzy', 'sandy', 'trews', 'mummy', 'kudzu', 'sissy',
             'stirk', 'poise', 'burns', 'pinky', 'amide', 'heath', 'spica', 'essay', 'worst', 'pygmy', 'fuggy', 'dross',
             'besot', 'rearm', 'curvy', 'loath', 'relic', 'butty', 'quack', 'angry', 'forge', 'gnome', 'stile', 'crown',
             'diner', 'awful', 'dwarf', 'gyrus', 'pulpy', 'gooey', 'boson', 'rover', 'toddy', 'marry', 'weald', 'thane',
             'shame', 'stank', 'liege', 'pewee', 'tours', 'lodge', 'lurid', 'surge', 'speak', 'dully', 'moray', 'agony',
             'swine', 'truck', 'foray', 'skill', 'sappy', 'album', 'floor', 'soggy', 'nerdy', 'smear', 'table', 'splay',
             'bobby', 'coypu', 'stone', 'gauze', 'shaft', 'gluey', 'blase', 'aspen', 'alibi', 'hymen', 'gamut', 'candy',
             'grove', 'algal', 'rouge', 'basis', 'bagel', 'plump', 'owing', 'scoff', 'pukka', 'yacht', 'chine', 'bijou',
             'nimby', 'adept', 'spine', 'sully', 'pylon', 'glaze', 'crest', 'ninon', 'fermi', 'until', 'stunk', 'silks',
             'swath', 'wings', 'punks', 'alula', 'tight', 'queen', 'annoy', 'elide', 'weber', 'crude', 'booty', 'sitar',
             'shone', 'hobby', 'claim', 'extra', 'maybe', 'spurn', 'guest', 'epoxy', 'canty', 'sabre', 'satyr', 'farce',
             'chill', 'gawky', 'chord', 'phial', 'macho', 'fluke', 'suite', 'organ', 'micro', 'homer', 'deign', 'twang',
             'waltz', 'abhor', 'cumin', 'scrap', 'latte', 'canna', 'slink', 'reset', 'fusee', 'quota', 'hardy', 'shred',
             'glume', 'panto', 'taste', 'geode', 'plier', 'polyp', 'parse', 'lurch', 'soapy', 'whisk', 'untie', 'facer',
             'there', 'aging', 'icing', 'boozy', 'coyly', 'elver', 'genie', 'whiff', 'store', 'grume', 'quest', 'prong',
             'joist', 'chasm', 'gayer', 'knock', 'saved', 'truss', 'mazer', 'islet', 'tawny', 'cater', 'liked', 'exult',
             'kurus', 'attic', 'tidal', 'grape', 'orate', 'karat', 'brill', 'cimex', 'spore', 'horny', 'gloom', 'cubit',
             'x-ray', 'penis', 'vowel', 'vault', 'paper', 'gamer', 'slain', 'cacti', 'resin', 'linen', 'tench', 'cocoa',
             'amass', 'salve', 'olive', 'addax', 'sorry', 'proud', 'azote', 'noise', 'belch', 'elect', 'ascus', 'chert',
             'troop', 'stoma', 'leggy', 'moire', 'apple', 'cross', 'scale', 'odium', 'extol', 'jetty', 'gumma', 'prion',
             'navel', 'molal', 'polar', 'cords', 'sound', 'vinyl', 'sleek', 'trend', 'mimic', 'crank', 'carat', 'felon',
             'gassy', 'layer', 'scuff', 'whelp', 'manga', 'melee', 'dhoti', 'ardeb', 'venom', 'boned', 'hyrax', 'stuck',
             'culex', 'frump', 'eagle', 'onset', 'amity', 'chose', 'minim', 'fussy', 'scrip', 'model', 'acned', 'forth',
             'tread', 'booth', 'thyme', 'badly', 'groin', 'broth', 'stern', 'slops', 'verso', 'bream', 'crick', 'cease',
             'piste', 'steer', 'lysin', 'guilt', 'hippy', 'spree', 'haiku', 'rower', 'filar', 'co-ed', 'chomp', 'kenaf',
             'fiend', 'whish', 'crook', 'ovine', 'seamy', 'parka', 'waxen', 'umbra', 'dwell', 'halon', 'lindy', 'flaky',
             'snare', 'rural', 'billy', 'spike', 'sonic', 'lemon', 'slant', 'saucy', 'lorry', 'chute', 'loyal', 'truth',
             'stuff', 'apian', 'enter', 'ivory', 'wring', 'vouch', 'nancy', 'curve', 'squat', 'beefy', 'lethe', 'farad',
             'jazzy', 'leach', 'marsh', 'sedge', 'loose', 'hitch', 'radii', 'beech', 'fizzy', 'nippy', 'beads', 'tacky',
             'blank', 'shirk', 'gully', 'vanda', 'grand', 'ditch', 'testa', 'crash', 'spang', 'alert', 'mined', 'eerie',
             'genus', 'karma', 'moped', 'beget', 'eject', 'feign', 'proxy', 'berry', 'nacho', 'scute', 'shrew', 'wrung',
             'snarl', 'hammy', 'stump', 'troat', 'slunk', 'inner', 'papal', 'stack', 'brash', 'hogan', 'stage', 'blain',
             'saner', 'shrug', 'start', 'fruit', 'dosed', 'milky', 'alder', 'showy', 'fried', 'least', 'spear', 'mango',
             'dowel', 'adder', 'oaten', 'belay', 'lasso', 'world', 'reify', 'bluer', 'creek', 'sport', 'maple', 'teeth',
             'abort', 'cocos', 'clang', 'kabob', 'unsex', 'empty', 'stoke', 'yokel', 'space', 'brake', 'blitz', 'angel',
             'dowse', 'irony', 'timid', 'china', 'sente', 'bench', 'madam', 'bound', 'amuck', 'glued', 'click', 'shall',
             'tryst', 'quiet', 'moron', 'petty', 'twirl', 'light', 'duvet', 'fetal', 'amaze', 'tough', 'serum', 'dozen',
             'cried', 'rinse', 'decry', 'abyss', 'matzo', 'loser', 'unzip', 'forte', 'round', 'liana', 'sinew', 'rondo',
             'elude', 'amine', 'paddy', 'emery', 'aglet', 'uvula', 'trial', 'gates', 'shawm', 'kasha', 'armet', 'shark',
             'whole', 'mills', 'stake', 'minus', 'stein', 'shard', 'chump', 'azoic', 'infix', 'vista', 'clasp', 'dried',
             'ulema', 'abode', 'cause', 'flier', 'harsh', 'khoum', 'lifer', 'tongs', 'pasty', 'droit', 'brier', 'joule',
             'awned', 'gazer', 'sedgy', 'snout', 'digit', 'jumbo', 'motif', 'stole', 'biome', 'drool', 'scour', 'daunt',
             'clerk', 'smell', 'broil', 'vogue', 'mover', 'could', 'outgo', 'epoch', 'larch', 'civet', 'loach', 'torah',
             'scald', 'aioli', 'ocean', 'amber', 'howdy', 'sieve', 'balmy', 'credo', 'elfin', 'costs', 'alien', 'mushy',
             'taken', 'socle', 'dodge', 'gruff', 'prawn', 'ready', 'pilaf', 'crypt', 'arise', 'thump', 'ninny', 'banks',
             'occur', 'delve', 'devil', 'thuja', 'cairn', 'meson', 'mount', 'canal', 'renal', 'vague', 'swirl', 'moved',
             'clued', 'eidos', 'prank', 'takin', 'lemur', 'laced', 'brute', 'align', 'saran', 'strut', 'allay', 'often',
             'fully', 'brink', 'chock', 'snips', 'agree', 'dixie', 'morph', 'pesto', 'glans', 'scull', 'canon', 'stoup',
             'xylem', 'agile', 'emcee', 'infer', 'float', 'skein', 'lemma', 'swash', 'brood', 'eager', 'tease', 'pearl',
             'ovary', 'amigo', 'quirk', 'crock', 'ahead', 'ninth']
    while True:
        won = False
        word = choice(WORDS)
        ind = 0

        location = {'1': '.Row-letter >> nth=0', '2': '.Row div:nth-child(2) >> nth=0',
                    '3': '.Row div:nth-child(3) >> nth=0',
                    '4': '.Row div:nth-child(4) >> nth=0', '5': '.Row div:nth-child(5) >> nth=0',
                    '6': '.game_rows div:nth-child(2) div >> nth=0',
                    '7': '.game_rows div:nth-child(2) div:nth-child(2)',
                    '8': '.game_rows div:nth-child(2) div:nth-child(3)',
                    '9': '.game_rows div:nth-child(2) div:nth-child(4)',
                    '10': '.game_rows div:nth-child(2) div:nth-child(5)',
                    '11': '.game_rows div:nth-child(3) div >> nth=0',
                    '12': '.game_rows div:nth-child(3) div:nth-child(2)',
                    '13': '.game_rows div:nth-child(3) div:nth-child(3)',
                    '14': '.game_rows div:nth-child(3) div:nth-child(4)',
                    '15': '.game_rows div:nth-child(3) div:nth-child(5)',
                    '16': '.game_rows div:nth-child(4) div >> nth=0',
                    '17': '.game_rows div:nth-child(4) div:nth-child(2)',
                    '18': '.game_rows div:nth-child(4) div:nth-child(3)',
                    '19': '.game_rows div:nth-child(4) div:nth-child(4)',
                    '20': '.game_rows div:nth-child(4) div:nth-child(5)',
                    '21': '.game_rows div:nth-child(5) div >> nth=0',
                    '22': '.game_rows div:nth-child(5) div:nth-child(2)',
                    '23': '.game_rows div:nth-child(5) div:nth-child(3)',
                    '24': '.game_rows div:nth-child(5) div:nth-child(4)',
                    '25': '.game_rows div:nth-child(5) div:nth-child(5)',
                    '26': '.game_rows div:nth-child(6) div >> nth=0',
                    '27': '.game_rows div:nth-child(6) div:nth-child(2)',
                    '28': '.game_rows div:nth-child(6) div:nth-child(3)',
                    '29': '.game_rows div:nth-child(6) div:nth-child(4)',
                    '30': '.game_rows div:nth-child(6) div:nth-child(5)'}
        existing = []
        correct_position = ['-' for i in range(5)]
        nope = []
        not_in_position = [list() for i in range(5)]

        for key, value in location.items():

            page.type(location[key], word[ind])
            if ind == 4:
                ind = 0
            else:
                ind += 1

            if int(key) % 5 == 0:
                page.keyboard.press('Enter')
                time.sleep(2)
                current = page.inner_html('div.game_rows')
                doc = BeautifulSoup(current, 'html.parser')
                l = doc.find_all('div', {'class', 'Row-locked-in'})
                if not l:
                    continue
                current = l[-1]

                letters = current.find_all('div', {'class': "Row-letter"})

                won_the_game = [i for i in letters if i['class'][-1] == 'letter-correct']
                if len(won_the_game) == 5:
                    time.sleep(2)
                    page.locator('button:has-text("Restart")').click()
                    won = True
                    won_games += 1
                    time.sleep(3)
                    break
                guessed_word = str()

                for index, i in enumerate(letters):
                    current_letter = i.text
                    for a in range(1, 10):
                        current_letter = current_letter.replace(str(a), '')
                    guessed_word += current_letter
                    state = i['class'][-1]

                    letter = i.text.replace('0', '')
                    for x in range(1, 9):
                        letter = letter.replace(str(x), '')
                    if state == 'letter-absent' and letter not in nope:
                        nope.append(letter)
                    elif state == 'letter-elsewhere' and letter not in existing:
                        existing.append(letter)
                        if letter not in not_in_position[index]:
                            not_in_position[index].append(letter)
                    elif state == 'letter-elsewhere':
                        if letter not in not_in_position[index]:
                            not_in_position[index].append(letter)
                    elif state == 'letter-correct':
                        correct_position[index] = letter
                        if letter not in existing:
                            existing.append(letter)
                if guessed_word != word:
                    page.locator('button:has-text("Give up")').click()
                    time.sleep(1)
                    page.locator('button:has-text("Restart")').click()
                    won = True
                    lost_games += 1
                    break

                lst = wordle_round(existing, correct_position, nope, words, not_in_position)
                if lst:
                    word, existing, correct_position, nope, words = lst
                    words.remove(word)
                else:
                    time.sleep(2)
                    page.locator('button:has-text("Give up")').click()
                    time.sleep(1)
                    page.locator('button:has-text("Restart")').click()
                    won = True
                    lost_games += 1
                    break
        if not won:
            time.sleep(1)
            page.locator('button:has-text("Restart")').click()
            lost_games += 1
            time.sleep(2)

        words = list(WORDS)
        print(f'WON : {won_games}')
        print(f"LOST : {lost_games}")
    browser.close()
