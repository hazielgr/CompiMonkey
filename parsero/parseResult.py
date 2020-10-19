##########################################
# PARSE RESULT
# La clase parseResult es para el resultado del parser
##############################################
class ParseResult:
	def __init__(self):
		self.error = None
		self.node = None
		self.move_count = 0

	def register_move(self):
		self.move_count += 1

	def register(self, res):
		self.move_count += res.move_count
		if res.error: self.error = res.error
		return res.node

	def success(self, node):
		self.node = node
		return self

	def failure(self, error):
		if not self.error or self.move_count == 0:
			self.error = error
		return self