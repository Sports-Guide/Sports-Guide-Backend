from rest_framework import serializers

from reports.models import Report


class ReportSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    latitude = serializers.DecimalField(
        max_digits=18,
        decimal_places=15,
        required=False
    )
    longitude = serializers.DecimalField(
        max_digits=18,
        decimal_places=15,
        required=False
    )
    area = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Report
        fields = [
            'report_type',
            'wrong_info',
            'latitude',
            'longitude',
            'other_info',
            'area',
            'images'
        ]
