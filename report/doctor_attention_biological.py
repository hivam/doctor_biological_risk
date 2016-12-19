# -*- coding: utf-8 -*-
# #############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import time
from openerp.report import report_sxw
from openerp import pooler
import logging
_logger = logging.getLogger(__name__)


class doctor_attention_biological(report_sxw.rml_parse):
	def __init__(self, cr, uid, name, context):
		super(doctor_attention_biological, self).__init__(cr, uid, name, context=context)
		self.localcontext.update({
			'time': time,
			'select_type': self.select_type,
			'select_type_attention': self.select_type_attention,
			'select_age': self.select_age,
			'mostrar_respuesta_si': self.mostrar_respuesta_si,
			'mostrar_respuesta_no': self.mostrar_respuesta_no,
			'selecciono_fecha': self.selecciono_fecha,
		})

	def select_type(self, tipo_usuario):
		if tipo_usuario:
			tipo = self.pool.get('doctor.tipousuario.regimen').browse(self.cr, self.uid, tipo_usuario).name
		else:
			tipo= None
		_logger.info(tipo)
		return tipo

	def select_type_attention(self, type_atention):
		context = {}
		context.update({'lang' : self.pool.get('res.users').browse(self.cr, self.uid, self.uid, context=context).lang})

		patient = self.pool.get('doctor.attentions.referral')
		type = dict(patient.fields_get(self.cr, self.uid, 'referral_ids',context=context).get('referral_ids').get('selection')).get(
			str(type_atention))
		return type


	def select_age(self, age):
		context = {}
		context.update({'lang' : self.pool.get('res.users').browse(self.cr, self.uid, self.uid, context=context).lang})
		attentions = self.pool.get('doctor.atencion.ries.bio')
		age_unit = dict(attentions.fields_get(self.cr, self.uid, 'age_unit',context=context).get('age_unit').get('selection')).get(
			str(age))
		return age_unit

	def mostrar_respuesta_si(self, seleccion):
		context = {}
		context.update({'lang' : self.pool.get('res.users').browse(self.cr, self.uid, self.uid, context=context).lang})
		respuesta = None	
		if seleccion:
			respuesta = 'Si'
		return respuesta

	def mostrar_respuesta_no(self, seleccion):
		context = {}
		context.update({'lang' : self.pool.get('res.users').browse(self.cr, self.uid, self.uid, context=context).lang})
		respuesta = None	
		if seleccion:
			respuesta = 'No'
		return respuesta	


	def selecciono_fecha(self, fecha):
		context = {}
		context.update({'lang' : self.pool.get('res.users').browse(self.cr, self.uid, self.uid, context=context).lang})
		respuesta = None
		if fecha:
			respuesta = fecha
		return respuesta	


report_sxw.report_sxw('report.doctor_attention_biological', 'doctor.atencion.ries.bio',
					  'addons/doctor_biological_risk/report/doctor_attention_biological.rml',
					  parser=doctor_attention_biological)
		
		
		
		
