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


	_name = 'doctor.atencion.ries.bio'
	_order = "date_attention desc"

	def button_closed(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'state': 'cerrada'}, context=context)

	def _get_profesional(self, cr, uid, ids, field_name, arg, context=None):
		res = {}
		professional_id = self.pool.get("doctor.professional").search(cr, uid, [('user_id', '=', uid)], context=context)
		for dato in self.browse(cr, uid, ids):
			
			for profesional in self.pool.get("doctor.professional").browse(cr, uid, professional_id, context=context):
	
				res[dato.id] = profesional.id
		return res


	def _get_especialidad(self, cr, uid, ids, field_name, arg, context=None):
		res = {}
		professional_id = self.pool.get("doctor.professional").search(cr, uid, [('user_id', '=', uid)], context=context)
		for dato in self.browse(cr, uid, ids):
			for profesional in self.pool.get("doctor.professional").browse(cr, uid, professional_id, context=context):
	
				res[dato.id] = profesional.speciality_id.id
		return res

	_columns = {

		'patient_id': fields.many2one('doctor.patient', 'Paciente', ondelete='restrict', readonly=True),
		'patient_photo': fields.related('patient_id', 'photo', type="binary", relation="doctor.patient", readonly=True),
		'date_attention': fields.datetime('Fecha de atencion', required=True, readonly=True),
		'origin': fields.char('Documento origen', size=64,
							  help="Reference of the document that produced this attentiont.", readonly=True),
		'professional_id': fields.function(_get_profesional, relation="doctor.professional", type="many2one", store=False,
									readonly=True, method=True, string="Profesional en la Salud"),
		'speciality': fields.function(_get_especialidad, relation="doctor.speciality", type="many2one", store=False,
									readonly=True, method=True, string="Especialidad"),
		'professional_photo': fields.related('professional_id', 'photo', type="binary", relation="doctor.professional",
											 readonly=True, store=False),
		'age_attention': fields.integer('Edad actual', readonly=True),
		'age_unit': fields.selection([('1', u'Años'), ('2', 'Meses'), ('3', 'Dias'), ], 'Unidad de medida de la edad',
									 readonly=True),
		'state': fields.selection([('abierta', 'Abierta'), ('cerrada', 'Cerrada')], 'Estado', readonly=True, required=True),

		'motivo_consulta': fields.char('Motivo de consulta', size=100, required=False, states={'closed': [('readonly', True)]}),
		'enfermedad_actual': fields.text('Enfermedad Actual', required=False, help="Enfermedad Actual",	 states={'closed': [('readonly', True)]}),
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
		'cierre_caso': fields.char('Cierre caso', states={'closed': [('readonly', True)]}),
		'plantilla_laboratorios_id': fields.many2one('doctor.attentions.recomendaciones', 'Plantillas', states={'closed': [('readonly', True)]}),
		'plantilla_tratamiento_id': fields.many2one('doctor.attentions.recomendaciones', 'Plantillas', states={'closed': [('readonly', True)]}),
		'plantilla_hallazgos_id': fields.many2one('doctor.attentions.recomendaciones', 'Plantillas', states={'closed': [('readonly', True)]}),
		'laboratorios_realizados': fields.one2many('doctor.attention.laboratorio', 'attentiont_id', 'Laboratorios Realizados',
											 ondelete='restrict', states={'closed': [('readonly', True)]}),
		'laboratorios_realizados_fuente': fields.one2many('doctor.attention.laboratorio_fuente', 'attentiont_id', 'Laboratorios Realizados a la Fuente',
											 ondelete='restrict', states={'closed': [('readonly', True)]}),

	}


	def onchange_patient(self, cr, uid, ids, patient_id, context=None):
		values = {}
		if not patient_id:
			return values
		patient_data = self.pool.get('doctor.patient').browse(cr, uid, patient_id, context=context)
		photo_patient = patient_data.photo

		values.update({
			'patient_photo': photo_patient,
			'age_attention' : self.calcular_edad(patient_data.birth_date),
			'age_unit' : self.calcular_age_unit(patient_data.birth_date)
		})
		return {'value': values}

	def onchange_professional(self, cr, uid, ids, professional_id, context=None):
		values = {}
		if not professional_id:
			return values
		professional_data = self.pool.get('doctor.professional').browse(cr, uid, professional_id, context=context)
		professional_img = professional_data.photo
		if professional_data.speciality_id.id:
			professional_speciality = professional_data.speciality_id.id
			values.update({
				'speciality': professional_speciality,
			})

		values.update({
			'professional_photo': professional_img,
		})
		return {'value': values}



	def calcular_edad(self,fecha_nacimiento):
		current_date = datetime.today()
		st_birth_date = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
		re = current_date - st_birth_date
		dif_days = re.days
		age = dif_days
		age_unit = ''
		if age < 30:
			age_attention = age,
			age_unit = '3'

		elif age > 30 and age < 365:
			age = age / 30
			age = int(age)
			age_attention = age,
			age_unit = '2'

		elif age >= 365:
			age = int((current_date.year-st_birth_date.year-1) + (1 if (current_date.month, current_date.day) >= (st_birth_date.month, st_birth_date.day) else 0))
			age_attention = age,
			age_unit = '1'
		
		return age

	def calcular_age_unit(self,fecha_nacimiento):
		current_date = datetime.today()
		st_birth_date = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
		re = current_date - st_birth_date
		dif_days = re.days
		age = dif_days
		age_unit = ''
		if age < 30:
			age_unit = '3'
		elif age > 30 and age < 365:
			age_unit = '2'

		elif age >= 365:
			age_unit = '1'

		return age_unit

	def onchange_plantillas(self, cr, uid, ids, plantilla_id, campo, context=None):
		res={'value':{}}
		_logger.info(plantilla_id)
		if plantilla_id:
			cuerpo = self.pool.get('doctor.attentions.recomendaciones').browse(cr,uid,plantilla_id,context=context).cuerpo
			res['value'][campo]=cuerpo
		else:
			res['value'][campo]=''
	
		return res



	def default_get(self, cr, uid, fields, context=None):
		res = super(doctor_atencion_riesgo_biol,self).default_get(cr, uid, fields, context=context)


		if context.get('active_model') == "doctor.patient":
			id_paciente = context.get('default_patient_id')
		else:
			id_paciente = context.get('patient_id')

		if id_paciente:    
			fecha_nacimiento = self.pool.get('doctor.patient').browse(cr,uid,id_paciente,context=context).birth_date
			res['age_attention'] = self.calcular_edad(fecha_nacimiento)
			res['age_unit'] = self.calcular_age_unit(fecha_nacimiento)
			
		#con esto cargams los items de revision por sistemas
		ids = self.pool.get('doctor.laboratorio').search(cr,uid,[('active','=',True)],context=context)
		registros = []
		registros_fuetes = []
		for i in self.pool.get('doctor.laboratorio').browse(cr,uid,ids,context=context):
			registros.append((0,0,{'laboratorio_id' : i.id,}))
			registros_fuetes.append((0,0,{'laboratorio_id' : i.id,}))
		#fin carga item revision sistemas

		res['laboratorios_realizados'] = registros
		res['laboratorios_realizados_fuente'] = registros_fuetes

		return res


	_defaults = {
		'date_attention': lambda *a: datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
		'state': 'abierta',
	}


	def write(self, cr, uid, ids, vals, context=None):

		if 'laboratorio_inicial_si' in vals:
			vals['laboratorio_inicial_si'] = True
			vals['laboratorio_inicial_no'] = False
		elif 'laboratorio_inicial_no' in vals:
			vals['laboratorio_inicial_si'] = False
			vals['laboratorio_inicial_no'] = True
		elif 'laboratorio_fuente_si' in vals:
			vals['laboratorio_fuente_si'] = True
			vals['laboratorio_fuente_no'] = False
		elif 'laboratorio_fuente_no' in vals:
			vals['laboratorio_inicial_si'] = False
			vals['laboratorio_inicial_no'] = True
		elif 'terapia_retroviral_si' in vals:
			vals['terapia_retroviral_si'] = True
			vals['terapia_retroviral_no'] = False
		elif 'terapia_retroviral_no' in vals:
			vals['laboratorio_inicial_si'] = False
			vals['terapia_retroviral_cual'] = ''
			vals['laboratorio_inicial_no'] = True
		elif 'presento_reaccion_terapia_si' in vals:
			vals['presento_reaccion_terapia_si'] = True
			vals['presento_reaccion_terapia_no'] = False
		elif 'presento_reaccion_terapia_no' in vals:
			vals['presento_reaccion_terapia_si'] = False
			vals['presento_reaccion_terapia_no'] = True		
	
		return super(doctor_atencion_riesgo_biol,self).write(cr, uid, ids, vals, context)


doctor_atencion_riesgo_biol()
