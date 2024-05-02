from rest_framework import serializers

class CurrencyConversionSerializer(serializers.Serializer):
    currency_from = serializers.ChoiceField(choices=['USD', 'GBP', 'EUR'])
    currency_to = serializers.ChoiceField(choices=['USD', 'GBP', 'EUR'])
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
