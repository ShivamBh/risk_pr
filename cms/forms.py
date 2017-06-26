from django import forms
from reports.models import Report, Country

class ReportForm(forms.ModelForm):
	class Meta:
		model = Report
		fields = (
			"location",
			"title",
			"summary",
			"assessment",
			"impact_tc",
			"advice",
			"event_bg_title",
			"event_bg_text",
			"latitude",
			"longitude",
			"impact_radius",
			"report_type",
					)