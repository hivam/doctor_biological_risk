# -*- coding: utf-8 -*-
##############################################################################
#
#	OpenERP, Open Source Management Solution
#	Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Affero General Public License as
#	published by the Free Software Foundation, either version 3 of the
#	License, or (at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU Affero General Public License for more details.
#
#	You should have received a copy of the GNU Affero General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import logging
_logger = logging.getLogger(__name__)
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import date, datetime, timedelta
from lxml import etree


class doctor_atencion_riesgo_biol(osv.osv):


	_name = 'doctor.attentions'
	_inherit = 'doctor.attentions'
	_order = "date_attention desc"



	def _get_especialidad(self, cr, uid, ids, field_name, arg, context=None):
		res = {}
		professional_id = self.pool.get("doctor.professional").search(cr, uid, [('user_id', '=', uid)], context=context)
		for dato in self.browse(cr, uid, ids):
			for profesional in self.pool.get("doctor.professional").browse(cr, uid, professional_id, context=context):
	
				res[dato.id] = profesional.speciality_id.id
		return res


	
	_columns = {

		'motivo_consulta': fields.char('Motivo de consulta', size=100, required=False, states={'closed': [('readonly', True)]}),
		'enfermedad_actual': fields.text('Enfermedad Actual', required=False, help="Enfermedad Actual",	 states={'closed': [('readonly', True)]}),
		'descripcion_accidente': fields.text(u'Descripción breve del accidente: ', help=u"Descripción breve del accidente", required=False, states={'closed': [('readonly', True)]}),
		'fecha_del_accidente': fields.datetime('Fecha del accidente', states={'closed': [('readonly', True)]}),
		'laboratorio_inicial_si': fields.boolean('Si', states={'closed': [('readonly', True)]}),
		'laboratorio_inicial_no': fields.boolean('No', states={'closed': [('readonly', True)]}),
		'laboratorio_fuente_si': fields.boolean('Si', states={'closed': [('readonly', True)]}),
		'laboratorio_fuente_no': fields.boolean('No', states={'closed': [('readonly', True)]}),
		'terapia_retroviral_si': fields.boolean('Si', states={'closed': [('readonly', True)]}),
		'terapia_retroviral_no': fields.boolean('No', states={'closed': [('readonly', True)]}),
		'terapia_retroviral_cual':fields.char(u'Cuál?', states={'closed': [('readonly', True)]}),
		'numero_de_terapias':fields.integer(u'Número de días de terapia antirretroviral', states={'closed': [('readonly', True)]},),
		'presento_reaccion_terapia_si':fields.boolean('Si', states={'closed': [('readonly', True)]}),
		'presento_reaccion_terapia_no':fields.boolean('No', states={'closed': [('readonly', True)]}),
		'antecedentes_personales_patolo':fields.char(u'Antecedentes personales / patológicos de importancia', states={'closed': [('readonly', True)]}),
		'signos_vitales_ids': fields.one2many('doctor.signos.vitales_riesgo_biol', 'attentiont_id', 'Tabla signos vitales', ondelete='restrict', states={'cerrada': [('readonly', True)]}),
		'hallazgos_positivos': fields.text('Hallazgos positivos al examen fisico', states={'closed': [('readonly', True)]}),
		'estado_esquema_vacunacion':fields.text(u'Estado del esquema de vacunación ', states={'closed': [('readonly', True)]}),
		'diagnostico':fields.text(u'Diagnóstico '),
		'diseases_ids': fields.one2many('doctor.attentions.diseases', 'attentiont_riesgo_id', 'Diseases', ondelete='restrict',
										states={'closed': [('readonly', True)]}),
		'origen_enfermedad_id':fields.many2one('doctor.origen.enfermedad', u'Origen de la enfermedad', states={'closed': [('readonly', True)]}),
		'tratamiento_recomendaciones': fields.text('Tratamiento y Recomendaciones', states={'closed': [('readonly', True)]}),
		'laboratorios_control': fields.text('Laboratorios de control', states={'closed': [('readonly', True)]}),
		'solicitud_consulta': fields.char('Solicitud consulta', states={'closed': [('readonly', True)]}),
		'speciality': fields.function(_get_especialidad, relation="doctor.speciality", type="many2one", store=False,
									readonly=True, method=True, string="Especialidad"),
		'cierre_caso': fields.char('Cierre caso', states={'closed': [('readonly', True)]}),
		'plantilla_laboratorios_id': fields.many2one('doctor.attentions.recomendaciones', 'Plantillas', states={'closed': [('readonly', True)]}),
		'plantilla_tratamiento_id': fields.many2one('doctor.attentions.recomendaciones', 'Plantillas', states={'closed': [('readonly', True)]}),
		'plantilla_hallazgos_id': fields.many2one('doctor.attentions.recomendaciones', 'Plantillas', states={'closed': [('readonly', True)]}),
		'laboratorios_realizados': fields.one2many('doctor.attention.laboratorio', 'attentiont_id', 'Laboratorios Realizados',
											 ondelete='restrict', states={'closed': [('readonly', True)]}),
		#'laboratorios_realizados_fuente': fields.one2many('doctor.attention.laboratorio.attentiont_id', 'attentiont_id', 'Laboratorios Realizados a la Fuente', ondelete='restrict', states={'closed': [('readonly', True)]}),

	}


	_defaults = {
		'date_attention': lambda *a: datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
		'state': 'abierta',
	}


	def create (cr, uid, vals, context=None):
		vals['tipo_historia']='hc_riesgo_biologico'
		res = super(doctor_atencion_riesgo_biol,self).create(cr, uid, vals, context)
		return res

doctor_atencion_riesgo_biol()
