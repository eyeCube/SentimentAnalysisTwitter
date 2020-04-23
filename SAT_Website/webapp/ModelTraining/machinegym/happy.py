
from .meta import *

EMOTES=(":d",":D","^_^",": d",">3",":)","(:","=)","(=","=D","8)","=]",
        "8d","8D","8P",":P",":p","=P","=p","^^","8^d",":')","=')",)

# (in order from highest to lowest match)
HASHTAGS='''#happiness #love #happy #life #smile #instagood #motivation #family
#photography #like #peace #instagram #inspiration #photooftheday #nature
#beautiful #joy #travel #friends #picoftheday #positivevibes #lifestyle
#fun #follow #goodvibes #selflove #beauty #art #bhfyp #health
#positivity #loveyourself #me #fashion #goals #fitness #music #blessed
#cute #christmas #gratitude #selfcare #likeforlikes #instadaily #freedom
#meditation #style #believe #grateful #mindfulness #memories #girl #photo
#friendship #wedding #selfie #passion #mindset #instalike #happinessishere
#happinessquotes #happinessisachoice #happinessis #happinessoverload
#happinessproject #happinesss #happinessiskey #happinesshomemade
#happinessdelight #happinessbeginstour #happinesseverywhere #happinessbegins
#happinessday #happinessisfree #happinesscomesfromwithin #happinessmood
#happinessinacup #happinessisthekey'''


DATA={
        'happy'         : C_C,
        'good'          : C_E,
        'bliss'         : C_B,
        'blissful'      : C_A,
        'cheer'         : C_D,
        'cheery'        : C_C,
        'cheerful'      : C_B,
        'content'       : C_D,
        'contented'     : C_C,
        'merry'         : C_B,
        'joy'           : C_B,
        'joyous'        : C_B,
        'joyful'        : C_B,
        'jovial'        : C_B,
        'jolly'         : C_B,
        'joking'        : C_C,
        'jocular'       : C_B,
        'glee'          : C_B,
        'gleeful'       : C_B,
        'carefree'      : C_B,
        'untroubled'    : C_B,
        'delighted'     : C_B,
        'smiling'       : C_B,
        'beaming'       : C_B,
        'grinning'      : C_B,
        'glowing'       : C_C,
        'satisfied'     : C_C,
        'gratified'     : C_C,
        'sunny'         : C_D,
        'radiant'       : C_D,
        'blithe'        : C_D,
        'blithesome'    : C_D,
        'beatific'      : C_A,
        'cock-a-hoop'   : C_C,
        'thrilled'      : C_C,
        'exuberant'     : C_A,
        'elated'        : C_B,
        'exhilerated'   : C_B,
        'ecstatic'      : C_A,
        'euphoric'      : C_A,
        'overjoyed'     : C_A,
        'exultant'      : C_B,
        'rapt'          : C_B,
        'rapture'       : C_B,
        'rapturous'     : C_B,
        'enraptured'    : C_B,
        'in seventh heaven' : C_B,
        'on cloud nine' : C_B,
        'over the moon' : C_B,
        'walking on air' : C_B,
        'beside myself' : C_B,
        'jumping for joy' : C_B,
        'chirpy'        : C_B,
        'sent'          : C_F,
        'chuffed'       : C_B,
        'as happy as Larry' : C_B,
        'as happy as a clam' : C_B,
        'made up'       : C_F,
        'wrapped'       : C_F,
        'gay'           : C_E,
        'jocose'        : C_B,
        'skippy'        : C_D,
        'fortunate'     : C_B,
        'lucky'         : C_D,
        'favorable'     : C_F,
        'advantageous'  : C_F,
        'opportune'     : C_F,
        'auspicious'    : C_E,
        'apt'           : C_E,
        'beneficial'    : C_D,
        'fitting'       : C_F,
        'befitting'     : C_D,
        'hallelujah'    : C_B,
        'praise'        : C_D,
        'worship'       : C_C,
        'jesus'         : C_D,
        'god'           : C_D,
        'heaven'        : C_C,
        'yay'        : C_C,
        'yayy'        : C_C,
        'celebration'        : C_C,
        'hooray'        : C_C,
        'hoorah'        : C_C,
        'yatta'        : C_C,
        'wee'        : C_C,
        'weee'        : C_C,
        'weeee'        : C_C,
        'weeeee'        : C_C,
        'loving'        : C_C,
        'lovin'        : C_C,
        'in love'        : C_C,
        'gay'        : C_C,
        'over the moon'        : C_C,
        'gouranga'        : C_C,
        'hb'        : C_C,
        'giddy'        : C_C,
        'buzzin'        : C_C,
        'khushi'        : C_C,
        'drunk'        : C_C,
        'laura'        : C_C,
        'ska'        : C_C,
        'hny'        : C_C,
        'happier than a pig in shit'        : C_C,
        'lewis'        : C_C,
        'weed'        : C_C,
        'effexor'        : C_C,
        'thc'        : C_C,
        'hhc'        : C_C,
        'ticked her fancy'        : C_C,
        'pwaa'        : C_C,
        'trappy'        : C_C,
        'farhan'        : C_C,
        'happles'        : C_C,
        'chuft'        : C_C,
        'thankee'        : C_C,
        'hff'        : C_C,
        'haps'        : C_C,
        'hannah'        : C_C,
        'artichoke'        : C_C,
        'shappy'        : C_C,
        'tight pants'        : C_C,
        'happiful'        : C_C,
        'shit'        : C_E,
        'katie'        : C_C,
        'boobies'        : C_C,
        'hngd'        : C_C,
        'merry'        : C_C,
        'excited'        : C_C,
        'gate massage'        : C_C,
        'feliz'        : C_C,
        'screwin'        : C_C,
        'roksolana'        : C_C,
        'reel big fish'        : C_C,
        'a_a'        : C_C,
        'plums'        : C_C,
        'lala'        : C_C,
        'supercalafragalisticespealladosecious'        : C_C,
        'minchy'        : C_C,
        'wicky'        : C_C,
        'happy holidays'        : C_B,
        'juiced'        : C_C,
        'tree spot'        : C_C,
        'humor'        : C_C,
        'rejoice'        : C_C,
        'he'        : C_C,
        'happies'        : C_C,
        'friday'        : C_C,
        'stinky weaselteats'        : C_C,
        'valentines day'        : C_C,
        'keng'        : C_C,
        'swankin'        : C_C,
        'hhd'        : C_C,
        'hailie jade'        : C_C,
        'syrett'        : C_C,
        'dwbh'        : C_C,
        's.h.i.t.'        : C_C,
        'happier'        : C_C,
        'fan'        : C_C,
        'owl city'        : C_C,
        'happy clam'        : C_C,
        'shadan'        : C_C,
        'haomin'        : C_C,
        'red letter day'        : C_C,
        'gruntled'        : C_C,
        'hth'        : C_C,
        'happy as a man with tits in his hat'        : C_C,
        'brappy'        : C_C,
    }
