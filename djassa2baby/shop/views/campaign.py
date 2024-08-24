from rest_framework import viewsets
from shop.models.campaign import Campaign
from shop.serializers.campaign import CampaignSerializer

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
