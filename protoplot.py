#!/usr/bin/env python


import os, sys
import json
import cairo
import math

def draw_hole( ctx, hole ):
	global bolded_holes
	if hole not in bolded_holes:
		ctx.set_source_rgb( 1, 0, 0 )
		bolded_holes.append( hole )
		ctx.arc( hole[0], hole[1], 8, 0, math.pi*2)
		ctx.stroke()
		

class Part( object ):
	def __init__( self, name, _type, x, y, orientation ):
		global packages, parts
		
		self.package = packages[ parts[ _type ]["package"] ]
		self.part = parts[ _type ]
		self.name = name
		self._type = _type
		
		self.x = x
		self.y = y
		self.orientation = orientation
		
		self.pins = {}
		
		self.notch = []

		self.rect = []
		
		self._compute_pins()
	
	def _compute_pins( self ):
		N = self.package["pins"] / 2
		
		# special case, one row package
		
		if self.package["width"] == 1:
			if self.orientation == "N":
				self.notch = ( 32 + self.x * 32, 32 + self.y * 32 - 16 )
				self.rect = ( 32 + self.x * 32 - 8 - 4, 
						  32 + self.y * 32-16, 
						  16 + 8, 32*N*2 )
				
				for i in range( self.package["pins"] ):
					px = 32 + self.x * 32
					py = 32 + self.y * 32 + i*32
					self.pins[i + 1] = (px, py)
			
			elif self.orientation == "S":
				self.notch = ( 32 + self.x * 32,  32 + self.y * 32 - 16 + self.package["pins"]*32 )
				self.rect = ( 32 + self.x * 32 - 8 - 4, 
						  32 + self.y * 32-16, 
						  16 + 8, 32*N*2 )
				
				for i in range( self.package["pins"] ):
					px = 32 + self.x * 32
					py = 32 + self.y * 32 + 32*(self.package["pins"] -  i - 1)
					self.pins[i + 1] = (px, py)
			
			elif self.orientation == "E":
				self.notch = ( 32 + self.x * 32 + 32*N*2 - 16 + 4 ,  32 + self.y * 32 )
				self.rect = ( 32 + self.x * 32 - 8 - 4, 
						  32 + self.y * 32-16, 
						  32*N*2,16 + 16 )
				
				for i in range( self.package["pins"] ):
					px = 32 + self.x * 32 + 32*(self.package["pins"] -  i - 1)
					py = 32 + self.y * 32
					self.pins[i + 1] = (px, py)					

			elif self.orientation == "W":
				self.notch = ( 32 + self.x * 32 - 16 ,  32 + self.y * 32 )
				self.rect = ( 32 + self.x * 32 - 8 - 8, 
						  32 + self.y * 32-16, 
						  32*N*2,16 + 16 )
				
				for i in range( self.package["pins"] ):
					px = 32 + self.x * 32 + 32*(self.package["pins"] -  i - 1)
					py = 32 + self.y * 32
					self.pins[i + 1] = (px, py)					
			
			return


		if self.package["width"] == 2:
			if self.orientation == "N":
				self.notch = ( 32 + self.x * 32 + 16, 32 + self.y * 32 - 16 )
				self.rect = ( 32 + self.x * 32 - 8 - 4, 
						  32 + self.y * 32-16, 
						  16 + 8+32, 32*N )
				
				for i in range( N ):
					px = 32 + self.x * 32
					py = 32 + self.y * 32 + i*32
					self.pins[i + 1] = (px, py)
				
				for i in range( N ):
					px = 32 + self.x * 32+32
					py = 32 + self.y * 32 + i*32
					self.pins[i + 1+N	] = (px, py)

			if self.orientation == "S":
				self.notch = ( 32 + self.x * 32 + 16, 32 + self.y * 32 - 16 + N*32 )
				self.rect = ( 32 + self.x * 32 - 8 - 4, 
						  32 + self.y * 32-16, 
						  16 + 8+32, 32*N )
				
				for i in range( N ):
					px = 32 + self.x * 32
					py = 32 + self.y * 32 + i*32
					self.pins[i + N  + 1] = (px, py)
				
				for i in range( N ):
					px = 32 + self.x * 32+32
					py = 32 + self.y * 32 + i*32
					self.pins[N - i] = (px, py)
		
			if self.orientation == "E":
				self.notch = ( 32 + self.x * 32 + 32*N - 16 + 4 ,  32 + self.y * 32 + 16 )
				self.rect = ( 32 + self.x * 32 - 8 - 4, 
						  32 + self.y * 32-16, 
						  32*N,16 + 16 + 32 )
				
				for i in range( N ):
					px = 32 + self.x * 32 + i*32
					py = 32 + self.y * 32
					self.pins[N - i] = (px, py)
				
				for i in range( N ):
					px = 32 + self.x * 32 + i*32
					py = 32 + self.y * 32 + 32
					self.pins[i + N + 1] = (px, py)

			if self.orientation == "W":
				self.notch = ( 32 + self.x * 32 - 16 + 4 ,  32 + self.y * 32 + 16 )
				self.rect = ( 32 + self.x * 32 - 8 - 4, 
						  32 + self.y * 32-16, 
						  32*N,16 + 16 + 32 )
				
				for i in range( N ):
					px = 32 + self.x * 32 + i*32
					py = 32 + self.y * 32
					self.pins[i + 1 + N] = (px, py)
				
				for i in range( N ):
					px = 32 + self.x * 32 + i*32
					py = 32 + self.y * 32 + 32
					self.pins[i + 1] = (px, py)
			
			
			return
		
		
		# package["width"] > 2
		
		if self.orientation == "N":
			self.notch = ( 32 + self.x * 32 + 32*(self.package["width"]-1)/2.0, 32 + self.y * 32 - 16 )
			
			self.rect = ( 32 + self.x * 32  + 8, 
						  32 + self.y * 32-16, 
						  32*(self.package["width"]-1) - 16, 32*N )
			
			for i in range( N ):
				px = 32 + self.x * 32
				py = 32 + self.y * 32 + i*32
				self.pins[i + 1] = (px, py)
			
			for i in range( N ):
				px = 32 + self.x * 32 + 32*(self.package["width"]-1)
				py = 32 + self.y * 32 + i*32
				self.pins[2*N - i] = (px, py)
			

		if self.orientation == "S":
			self.notch = ( 32 + self.x * 32 + 32*(self.package["width"]-1)/2.0, 32 + self.y * 32 - 16 + N*32 )
			
			self.rect = ( 32 + self.x * 32  + 8, 
						  32 + self.y * 32-16, 
						  32*(self.package["width"]-1) - 16, 32*N )
			
			for i in range( N ):
				px = 32 + self.x * 32
				py = 32 + self.y * 32 + i*32
				self.pins[i + N + 1] = (px, py)
				
			
			for i in range( N ):
				px = 32 + self.x * 32 + 32*(self.package["width"]-1)
				py = 32 + self.y * 32 + i*32
				self.pins[N - i] = (px, py)


		if self.orientation == "E":
			self.notch = ( 32 + self.x * 32 + 32*N - 16 - 8, 32 + self.y * 32  + 32*(self.package["width"]-1)/2.0 )
			
			self.rect = ( 32 + self.x * 32 - 8, 
						  32 + self.y * 32+8, 
						  32*N - 16, 32*(self.package["width"]-1) - 16 )
			
			for i in range( N ):
				px = 32 + self.x * 32 + i*32
				py = 32 + self.y * 32
				self.pins[N - i] = (px, py)
			
			for i in range( N ):
				px = 32 + self.x * 32 + i*32
				py = 32 + self.y * 32 + 32*(self.package["width"]-1)
				self.pins[i + N + 1] = (px, py)
	
		if self.orientation == "W":
			self.notch = ( 32 + self.x * 32 - 8, 32 + self.y * 32  + 32*(self.package["width"]-1)/2.0 )
			
			self.rect = ( 32 + self.x * 32 - 8, 
						  32 + self.y * 32+8, 
						  32*N - 16, 32*(self.package["width"]-1) - 16 )
			
			for i in range( N ):
				px = 32 + self.x * 32 + i*32
				py = 32 + self.y * 32
				self.pins[2*N - i] = (px, py)
			
			for i in range( N ):
				px = 32 + self.x * 32 + i*32
				py = 32 + self.y * 32 + 32*(self.package["width"]-1)
				self.pins[i + 1] = (px, py)

			
	def draw( self, ctx ):
		ctx.set_source_rgb( 1, 1, 1 )
		ctx.rectangle( *self.rect )
		ctx.fill()
		
		ctx.set_source_rgb( 0.1, 0.1, 0.1 )
		ctx.rectangle( *self.rect )
		ctx.stroke()
		
		if self.orientation == "N":
			ctx.arc( self.notch[0], self.notch[1], 8, 0, math.pi )
			ctx.stroke()
		
		elif self.orientation == "S":
			ctx.arc( self.notch[0], self.notch[1], 8, math.pi, math.pi*2 )
			ctx.stroke()

		elif self.orientation == "E":
			ctx.arc( self.notch[0], self.notch[1], 8, math.pi/2, math.pi*3/2.0 )
			ctx.stroke()

		elif self.orientation == "W":
			ctx.arc( self.notch[0], self.notch[1], 8, math.pi*2 - math.pi/2, math.pi*2 - math.pi*3/2.0 )
			ctx.stroke()
		
		
		for pin_id in self.pins:
			hole = self.pins[pin_id]
			
			draw_hole( ctx, hole )
		
		
		#pins
		N = self.package["pins"] / 2
		
		#if self.package["width"] == 2:
		#	if self.orientation == "N":
		#		for i in range( N ):
		#			(px,py) = self.pins[i+1]
		#			px -= ctx.text_extents(self.part["pins"][i])[2] + 16
		#			py += 4
		#			ctx.move_to( px, py )
		#			ctx.show_text( self.part["pins"][i] )
		#			ctx.stroke()
		#		
		#		for i in range( N ):
		#			continue
		#			(px,py) = self.pins[i + 1 + N]
		#			px -= ctx.text_extents( self.part["pins"][i+N] )[2] + 12
		#			py += 4
		#			ctx.move_to( px, py )
		#			ctx.show_text( self.part["pins"][i+N] )
		#			ctx.stroke()
		#	return
		
		if self.orientation == "N":
			for i in range( N ):
				(px,py) = self.pins[i+1]
				px += 12
				py += 4
				ctx.move_to( px, py )
				ctx.show_text( self.part["pins"][i] )
				ctx.stroke()
			
			for i in range( N ):
				(px,py) = self.pins[i + 1 + N]
				px -= ctx.text_extents( self.part["pins"][i+N] )[2] + 12
				py += 4
				ctx.move_to( px, py )
				ctx.show_text( self.part["pins"][i+N] )
				ctx.stroke()
				
		if self.orientation == "S":
			for i in range( N ):
				(px,py) = self.pins[i+1]
				px -= ctx.text_extents( self.part["pins"][i] )[2] + 12
				py += 4
				ctx.move_to( px, py )
				ctx.show_text( self.part["pins"][i] )
				ctx.stroke()
			
			for i in range( N ):
				(px,py) = self.pins[i + 1 + N]
				px += 12
				py += 4
				ctx.move_to( px, py )
				ctx.show_text( self.part["pins"][i + N] )
				ctx.stroke()
			
		if self.orientation == "E":
			for i in range( N ):
				(px,py) = self.pins[i+1]
				#px -= ctx.text_extents( self.part["pins"][i] )[2] + 12
				#py += 4
				#ctx.move_to( px, py )
				ctx.save()
				ctx.translate( px, py )
				ctx.rotate( math.pi/2)
				ctx.move_to( 12, 4 )
				ctx.show_text( self.part["pins"][i] )
				ctx.stroke()
				ctx.restore()

			for i in range( N ):
				(px,py) = self.pins[i+1 + N]
				#px -= ctx.text_extents( self.part["pins"][i] )[2] + 12
				#py += 4
				#ctx.move_to( px, py )
				ctx.save()
				ctx.translate( px, py )
				ctx.rotate( math.pi/2)
				ctx.move_to( -ctx.text_extents( self.part["pins"][i+N] )[2] - 12, 4 )
				ctx.show_text( self.part["pins"][i + N] )
				ctx.stroke()
				ctx.restore()
		
		if self.orientation == "W":
			for i in range( N ):
				(px,py) = self.pins[i+1]
				#px -= ctx.text_extents( self.part["pins"][i] )[2] + 12
				#py += 4
				#ctx.move_to( px, py )
				ctx.save()
				ctx.translate( px, py )
				ctx.rotate( -math.pi/2)
				ctx.move_to( 12, 4 )
				ctx.show_text( self.part["pins"][i] )
				ctx.stroke()
				ctx.restore()

			for i in range( N ):
				(px,py) = self.pins[i+1 + N]
				#px -= ctx.text_extents( self.part["pins"][i] )[2] + 12
				#py += 4
				#ctx.move_to( px, py )
				ctx.save()
				ctx.translate( px, py )
				ctx.rotate( -math.pi/2)
				ctx.move_to( -ctx.text_extents( self.part["pins"][i+N] )[2] - 12, 4 )
				ctx.show_text( self.part["pins"][i + N] )
				ctx.stroke()
				ctx.restore()

def parse_line( symbols, line ):
	out = []
	for value in line:
		if value.isdigit():
			out.append( 32 + 32*int( value ) )
		else:
			(key, pin) = value.split( "." )
			pin = int(pin)
			part = symbols[key]
			out.extend( list( part.pins[pin] ) )
	
	pairs = []
	for i in range( 0, len( out ), 2 ):
		pairs.append( (out[i], out[i+1]) )
	return pairs
	
				

fname = sys.argv[1]

packages = {}
boards = {}
parts = {}

with open( "packages.json", "r" ) as handle:
	txt = handle.read()
	packages = json.loads( txt )

with open( "boards.json", "r" ) as handle:
	txt = handle.read()
	boards = json.loads( txt )

with open( "parts.json", "r" ) as handle:
	txt = handle.read()
	parts = json.loads( txt )


lines = []

with open( sys.argv[1], "r" ) as handle:
	for row in handle:
		row = row.strip()
		if "#" in row:
			idx = row.find("#")
			row = row[:idx]
			row = row.strip()
		if len( row ) < 1:
			continue
		lines.append( row.split() )

board = ""
for line in lines:
	if line[0] == "board":
		board = line[1]


board_width = boards[board]["width"]
board_height = boards[board]["height"]

symbols = {}

WIDTH =  32 * (board_width + 1)
HEIGHT = 32 * (board_height + 1)



surface = cairo.ImageSurface( cairo.FORMAT_ARGB32, WIDTH, HEIGHT )
ctx = cairo.Context( surface )

ctx.set_source_rgb( 1, 1, 1 )
ctx.rectangle( 0, 0, WIDTH, HEIGHT )
ctx.fill()

ctx.set_source_rgb( 1, 0.9, 0.9	 )

for x in range( board_width ):
	for y in range( board_height ):
		px = 32 + 32*x
		py = 32 + 32*y
		
		ctx.arc( px, py, 8, 0, math.pi*2 )
		ctx.stroke()


bolded_holes = []


for line in lines:
	if line[0] == "part":
		#symbols[ line[1] ] = line[2:]
		symbols[ line[1] ] = Part( line[1], line[2], int( line[3] ) - 1, int( line[4] ) - 1, line[5] )
		
		symbols[ line[1] ].draw( ctx )

	elif line[0] == "wire":
		(start, stop) = parse_line( symbols, line[1:] )
		

		draw_hole( ctx, tuple( start ) )
		draw_hole( ctx, tuple( stop ) )
		

		ctx.set_source_rgb( 0, 0, 1 )
		ctx.move_to( *start )
		ctx.line_to( *stop )
		ctx.stroke()

	elif line[0] == "resistor":

		(start, stop) = parse_line( symbols, line[1:] )
		
		draw_hole( ctx, tuple( start ) )
		draw_hole( ctx, tuple( stop ) )
		

		dx = stop[0] - start[0]
		dy = stop[1] - start[1]
		
		midpoint = (start[0] + 0.5 * dx, start[1] + 0.5 * dy)
		
		ld = math.sqrt( dx*dx + dy*dy )
		
		ndx = dx/ld
		ndy = dy/ld
		
		r_0 = ( midpoint[0] - 32*ndx, midpoint[1] - 32*ndy )
		r_1 = ( midpoint[0] + 32*ndx, midpoint[1] + 32*ndy )
		
		
		ctx.set_source_rgb( 0, 1, 0 )
		
		ctx.move_to( *start )
		ctx.line_to( *r_0 )
		ctx.stroke()
		
		ctx.move_to( *r_1 )
		ctx.line_to( *stop )
		ctx.stroke()
		
		normx = -ndy
		normy = ndx
		
		r_00 = ( r_0[0] + normx*16, r_0[1] + normy*16 )
		r_01 = ( r_0[0] - normx*16, r_0[1] - normy*16 )	
		
		ctx.move_to( *r_00 )
		ctx.line_to( *r_01 )
		ctx.stroke()
		
		r_10 = ( r_1[0] + normx*16, r_1[1] + normy*16 )
		r_11 = ( r_1[0] - normx*16, r_1[1] - normy*16 )	
		
		ctx.move_to( *r_10 )
		ctx.line_to( *r_11 )
		ctx.stroke()
		
		ctx.move_to( *r_00 )
		ctx.line_to( *r_10 )
		ctx.stroke()
		
		ctx.move_to( *r_01 )
		ctx.line_to( *r_11 )
		ctx.stroke()

	elif line[0] == "capacitor":
		(start, stop) = parse_line( symbols, line[1:] )

		draw_hole( ctx, tuple( start ) )
		draw_hole( ctx, tuple( stop ) )
		

		#ctx.set_source_rgb( 0, 0, 1 )
		#ctx.move_to( *start )
		#ctx.line_to( *stop )
		#ctx.stroke()
		
		dx = stop[0] - start[0]
		dy = stop[1] - start[1]
		
		midpoint = (start[0] + 0.5 * dx, start[1] + 0.5 * dy)
		
		ld = math.sqrt( dx*dx + dy*dy )
		
		ndx = dx/ld
		ndy = dy/ld
		
		r_0 = ( midpoint[0] - 10*ndx, midpoint[1] - 10*ndy )
		r_1 = ( midpoint[0] + 10*ndx, midpoint[1] + 10*ndy )
		
		
		ctx.set_source_rgb( 0, 0.7, 0 )
		
		ctx.move_to( *start )
		ctx.line_to( *r_0 )
		ctx.stroke()
		
		ctx.move_to( *r_1 )
		ctx.line_to( *stop )
		ctx.stroke()
		
		normx = -ndy
		normy = ndx
		
		r_00 = ( r_0[0] + normx*30, r_0[1] + normy*30 )
		r_01 = ( r_0[0] - normx*30, r_0[1] - normy*30 )	
		
		ctx.move_to( *r_00 )
		ctx.line_to( *r_01 )
		ctx.stroke()
		
		r_10 = ( r_1[0] + normx*30, r_1[1] + normy*30 )
		r_11 = ( r_1[0] - normx*30, r_1[1] - normy*30 )	
		
		ctx.move_to( *r_10 )
		ctx.line_to( *r_11 )
		ctx.stroke()
		
		
		
(head, tail) = os.path.split( fname )
fn = tail.split(".")[0]

surface.write_to_png( fn + ".png" )
