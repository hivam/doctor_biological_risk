# -*- coding: utf-8 -*-
##############################################################################
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
##############################################################################

{
    'name'        : 'Doctor_riesgo_biologico',
    'version'     : '1.0',
    'summary'     : 'crear historia clinica de riesgo biologico',
    'description' : 'Doctor_riesgo_biologico agrega la posibilidad de que el consultorio o entidad de salud cuente con una historia de riesgo biologico',
    'category'    : 'medical',
    'author'      : 'Proyecto Evoluzion',
    'website'     : 'http://www.proyectoevoluzion.com/',
    'license'     : 'AGPL-3',
    'depends'     : ['l10n_co_doctor'],
    'data'        : [
                    'security/ir.model.access.csv',
                    #'views/doctor_atencion_riesgo_biologico_view.xml',
                    'views/doctor_signos_vitales_view.xml',
                    'views/doctor_origen_enfermedad_view.xml',
                    'data/tipo_cita_riesgo.sql',
                    'data/laboratorios_data.xml',
                    'views/doctor_report_biological.xml',
                    'views/prueba_view.xml'

    ],      
    'installable' : True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
