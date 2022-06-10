from pyexpat import model
from rest_framework.serializers import *
from .models import *

class SaveSerializer(ModelSerializer):
    class Meta:
        model=SaveAnalysis
        fields = '__all__'



