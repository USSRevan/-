import enum

class ScanningStage(enum.Enum):
	move = 0
	scan = 1
	grab = 2
	throw = 3