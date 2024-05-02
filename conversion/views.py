from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CurrencyConversionSerializer
from decimal import Decimal

class CurrencyConversionAPI(APIView):
    def get(self, request, currency_from, currency_to, amount, *args, **kwargs):
        # Convert amount to Decimal
        amount_decimal = Decimal(amount)

        # Create a dictionary with the URL parameters
        data = {
            'currency_from': currency_from,
            'currency_to': currency_to,
            'amount': amount_decimal  # Use the converted Decimal amount
        }

        # Pass the data to the serializer
        serializer = CurrencyConversionSerializer(data=data)

        # Validate the serializer
        if serializer.is_valid():
            # Extract validated data from the serializer
            currency_from = serializer.validated_data['currency_from']
            currency_to = serializer.validated_data['currency_to']
            amount = serializer.validated_data['amount']

            # Perform currency conversion logic here
            # For demonstration, assuming 1:1 conversion for simplicity
            conversion_rates = {'USD': {'USD': Decimal('1'), 'GBP': Decimal('0.72'), 'EUR': Decimal('0.83')},
                                'GBP': {'USD': Decimal('1.39'), 'GBP': Decimal('1'), 'EUR': Decimal('1.16')},
                                'EUR': {'USD': Decimal('1.21'), 'GBP': Decimal('0.86'), 'EUR': Decimal('1')}}
            conversion_rate = conversion_rates[currency_from][currency_to]
            converted_amount = amount * conversion_rate

            # Return the response with converted amount
            return Response({'currency_from': currency_from, 'currency_to': currency_to, 'amount': amount, 'converted_amount': converted_amount}, status=status.HTTP_200_OK)

        # If serializer validation fails, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
