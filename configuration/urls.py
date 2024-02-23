from django.urls import path
from configuration.views import *

app_name = 'configuration'

urlpatterns = [

    # employee
    path('epm/', EmployeeListView.as_view(), name='EmployeeListView'),
    path('add/', EmployeeCreateView.as_view(), name='EmployeeCreateView'),
    path('employeeedit/edit/<pk>/', EmployeeUpdateView.as_view(), name='EmployeeUpdateView'),
    path('employeeedit/delete/<pk>/', EmployeeDeleteView.as_view(), name='EmployeeDeleteView'),

    # confirmation-increment-noincrement
    path('confirmationincrementnoincrement/', ConfirmationIncrementNoincrementListView.as_view(), name='ConfirmationIncrementNoincrementListView'),
    path('confirmationincrementnoincrementadd/', ConfirmationIncrementNoincrementCreateView.as_view(), name='ConfirmationIncrementNoincrementCreateView'),
    path('confirmationincrementnoincrementedit/edit/<pk>/', ConfirmationIncrementNoincrementUpdateView.as_view(), name='ConfirmationIncrementNoincrementUpdateView'),

    # sbu
    path('sbu/', SBUListView.as_view(), name='SBUListView'),
    path('sbuadd/', SBUCreateView.as_view(), name='SBUCreateView'),
    path('sbuedit/edit/<pk>/', SBUUpdateView.as_view(), name='SBUUpdateView'),
    #path('sbuedit/delete/<pk>/',  SBUDeleteView.as_view(), name='SBUDeleteView'),

    # sub-sbu
    path('subsbu/', SubSBUListView.as_view(), name='SubSBUListView'),
    path('subsbuadd/', SubSBUCreateView.as_view(), name='SubSBUCreateView'),
    path('subsbuedit/edit/<pk>/', SubSBUUpdateView.as_view(), name='SubSBUUpdateView'),
    #path('subsbuedit/delete/<pk>/', SubSBUDeleteView.as_view(), name='SubSBUDeleteView'),

    # sbu-director-name
    path('sbudirectorname/', SBUDirectorNameListView.as_view(), name='SBUDirectorNameListView'),
    path('sbudirectornameadd/', SBUDirectorNameCreateView.as_view(), name='SBUDirectorNameCreateView'),
    path('sbudirectornameedit/edit/<pk>/', SBUDirectorNameUpdateView.as_view(), name='SBUDirectorUpdateNameView'),

    # supervisor
    path('supervisor/', SupervisorListView.as_view(), name='SupervisorListView'),
    path('supervisoradd/', SupervisorCreateView.as_view(), name='SupervisorCreateView'),
    path('supervisoredit/edit/<pk>/', SupervisorUpdateView.as_view(), name='SupervisorUpdateView'),
    #path('supervisoredit/delete/<pk>/', SupervisorDeleteView.as_view(), name='SupervisorDeleteView'),

    # project
    path('project/', ProjectListView.as_view(), name='ProjectListView'),
    path('projectadd/', ProjectCreateView.as_view(), name='ProjectCreateView'),
    path('projectedit/edit/<pk>/', ProjectUpdateView.as_view(), name='ProjectUpdateView'),
    #path('projectedit/delete/<pk>/', ProjectDeleteView.as_view(), name='ProjectDeleteView'),

    # review-rating
    path('reviewrating/', ReviewRatingListView.as_view(), name='ReviewRatingListView'),
    path('reviewratingadd/', ReviewRatingCreateView.as_view(), name='ReviewRatingCreateView'),
    path('reviewratingedit/edit/<pk>/', ReviewRatingUpdateView.as_view(), name='ReviewRatingUpdateView'),
    #path('reviewratingedit/delete/<pk>/', ReviewRatingDeleteView.as_view(), name='ReviewRatingDeleteView'),

    # kpi-configuration
    path('kpiconfig/', KPIConfigListView.as_view(), name='KPIConfigListView'),
    path('kpiconfigadd/', KPIConfigCreateView.as_view(), name='KPIConfigCreateView'),
    path('kpiconfigedit/edit/<pk>/', KPIConfigUpdateView.as_view(), name='KPIConfigUpdateView'),
    #path('kpiconfigedit/delete/<pk>/', KPIConfigDeleteView.as_view(), name='KPIConfigDeleteView'),

    # evaluation
    path('evaluation/', EvaluationListView.as_view(), name='EvaluationListView'),
    path('evaluationuadd/', EvaluationCreateView.as_view(), name='EvaluationCreateView'),
    path('evaluationedit/edit/<pk>/', EvaluationUpdateView.as_view(), name='EvaluationUpdateView'),

    # kpi-objective
    path('kpiobjective/', KPIObjectiveListView.as_view(), name='KPIObjectiveListView'),
    path('kpiobjectiveuadd/', KPIObjectiveCreateView.as_view(), name='KPIObjectiveCreateView'),
    path('kpiobjectiveedit/edit/<pk>/', KPIObjectiveUpdateView.as_view(), name='KPIObjectiveUpdateView'),

    # kpi-value
    path('kpivalue/', KPIValueListView.as_view(), name='KPIValueListView'),
    path('kpivalueadd/', KPIValueCreateView.as_view(), name='KPIValueCreateView'),
    path('kpivalueedit/edit/<pk>/', KPIValueUpdateView.as_view(), name='KPIValueUpdateView'),

    # hr-rating
    path('hrrating/', HRRatingListView.as_view(), name='HRRatingListView'),
    path('hrratingadd/', HRRatingCreateView.as_view(), name='HRRatingCreateView'),
    path('hrratingedit/edit/<pk>/', HRRatingUpdateView.as_view(), name='HRRatingUpdateView'),

    # criticality
    path('criticality/', CriticalityListView.as_view(), name='CriticalityListView'),
    path('criticalityadd/', CriticalityCreateView.as_view(), name='CriticalityCreateView'),
    path('criticalityedit/edit/<pk>/', CriticalityUpdateView.as_view(), name='CriticalityUpdateView'),

    # potential-for-improvement
    path('potentialforimprovement/', PotentialForImprovementListView.as_view(), name='PotentialForImprovementListView'),
    path('potentialforimprovementadd/', PotentialForImprovementCreateView.as_view(), name='PotentialForImprovementCreateView'),
    path('potentialforimprovementedit/edit/<pk>/', PotentialForImprovementUpdateView.as_view(), name='PotentialForImprovementUpdateView'),

    # technical-implementation-operational
    path('technicalimplementationoperational/', TechnicalImplementationOperationalListView.as_view(), name='TechnicalImplementationOperationalListView'),
    path('technicalimplementationoperationaladd/', TechnicalImplementationOperationalCreateView.as_view(), name='TechnicalImplementationOperationalCreateView'),
    path('technicalimplementationoperationaledit/edit/<pk>/', TechnicalImplementationOperationalUpdateView.as_view(), name='TechnicalImplementationOperationalUpdateView'),

    # top-average-bottom performer
    path('topaveragebottomperformer/', TopAverageBottomPerformerListView.as_view(), name='TopAverageBottomPerformerListView'),
    path('topaveragebottomperformeradd/', TopAverageBottomPerformerCreateView.as_view(), name='TopAverageBottomPerformerCreateView'),
    path('topaveragebottomperformeredit/edit/<pk>/', TopAverageBottomPerformerUpdateView.as_view(), name='TopAverageBottomPerformerUpdateView'),

    # best-performer-team
    path('bestperformerteam/', BestPerformerTeamListView.as_view(), name='BestPerformerTeamListView'),
    path('bestperformerteamadd/', BestPerformerTeamCreateView.as_view(), name='BestPerformerTeamCreateView'),
    path('bestperformerteamedit/edit/<pk>/', BestPerformerTeamUpdateView.as_view(), name='BestPerformerTeamUpdateView'),

    # best-performer-organization
    path('bestperformerorganization/', BestPerformerOrganizationListView.as_view(), name='BestPerformerOrganizationListView'),
    path('bestperformerorganizationadd/', BestPerformerOrganizationCreateView.as_view(), name='BestPerformerOrganizationCreateView'),
    path('bestperformerorganizationedit/edit/<pk>/', BestPerformerOrganizationUpdateView.as_view(), name='BestPerformerOrganizationUpdateView'),

    # best-performer-pm
    path('bestperformerpm/', BestPerformerPMListView.as_view(), name='BestPerformerPMListView'),
    path('bestperformerpmadd/', BestPerformerPMCreateView.as_view(), name='BestPerformerPMCreateView'),
    path('bestperformerpmedit/edit/<pk>/', BestPerformerPMUpdateView.as_view(), name='BestPerformerPMUpdateView'),

    # best-innovator-team
    path('bestinnovatorteam/', BestInnovatorTeamListView.as_view(), name='BestInnovatorTeamListView'),
    path('bestinnovatorteamadd/', BestInnovatorTeamCreateView.as_view(), name='BestInnovatorTeamCreateView'),
    path('bestinnovatorteamedit/edit/<pk>/', BestInnovatorTeamUpdateView.as_view(), name='BestInnovatorTeamUpdateView'),

]