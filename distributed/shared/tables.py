__author__ = 'civa'

OBJECT_TYPES = dict(STAR=0, CATALOG_STAR=1, PLANET=2, OPEN_CLUSTER=3, GLOBULAR_CLUSTER=4,
	GASEOUS_NEBULA=5, PLANETARY_NEBULA=6, SUPERNOVA_REMNANT=7, GALAXY=8,
	COMET=9, ASTEROID=10, CONSTELLATION=11, MOON=12, ASTERISM=13,
	GALAXY_CLUSTER=14, DARK_NEBULA=15, QUASAR=16, MULT_STAR=17, RADIO_SOURCE=18,
	SATELLITE=19, SUPERNOVA=20, UNKNOWN=99)
OBJECT_TYPE_MAPS = [
	(['*iC','*iN','*iA','*i*','V*?','Pe*','HB*','Y*O','Ae*','Em*','Be*','BS*','RG*','AB*','C*','S*','sg*','s*r','s*y','s*b','pA*','WD*','ZZ*','LM*','BD*','N*','OH*','CH*','pr*','TT*','WR*','PM*','HV*','V* ','Ir*','Or*','RI*','Er*','Fl*','FU*','RC*','RC?','Ro*','a2*','Psr','BY*','RS*','Pu*','RR*','Ce*','dS*','RV*','WV*','bC*','cC*','gD*','SX*','LP*','Mi*','sr*','SN*','su*','Pl?','Pl'], 'STAR'),
	#([''], 'CATALOG_STAR'),
	(['Pl?', 'Pl'], 'PLANET'),
	(['OpC', 'C?*', 'OpC'], 'OPEN_CLUSTER'),
	(['GlC', 'Gl?'], 'GLOBULAR_CLUSTER'),
	('GNe,BNe,RNe,MoC,glb,cor,SFR,HVC,HII'.split(','), 'GASEOUS_NEBULA'),
	(['PN','PN?'], 'PLANETARY_NEBULA'),
	(['SR?', 'SNR'], 'SUPERNOVA_REMNANT'),
	('IG,PaG,G,PoG,GiC,BiC,GiG,GiP,HzG,ALS,LyA,DLA,mAL,LLS,BAL,rG,H2G,LSB,LeI,LeG,LeQ,EmG,SBG,bCG'.split(','), 'GALAXY'),
	('SCG,ClG,GrG,CGG'.split(','), 'GALAXY_CLUSTER'),
	(['DNe'], 'DARK_NEBULA'),
	('AGN,LIN,SyG,Sy1,Sy2,Bla,BLL,OVV,QSO,AG?,Q?,Bz?,BL?'.split(','), 'QUASAR'),
	(['LXB,HXB, As*,St*,MGr,**,EB*,Al*,bL*,WU*,EP*,SB*,El*,Sy*,CV*,DQ*,AM*,NL*,No*,DN*,XB*,LXB,HXB'], 'MULT_STAR'),
	('Rad,mR,cm,mm,smm'.split(','), 'RADIO_SOURCE'),
	(['SN?', 'SN*'], 'SUPERNOVA'),
	# ([''], 'SATELLITE'), # no satellites in Simbad, they don't have fixed positions
	#([''], 'COMET'),
	#([''], 'ASTEROID'),
	#([''], 'CONSTELLATION'),
	#([''], 'MOON'),
	#([''], 'ASTERISM'),
]