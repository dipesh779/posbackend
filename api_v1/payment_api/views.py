from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
# from payment.models import bill_stock

from .serializers import InvoiceSerializer, InvoiceListSerializer, CustomerInvoiceHelperSerializer, \
                        VendorPaymentListSerializer, VendorPaymentUpdateSerializer
from employee.utils.token_helper import token_helper, token_helper_employee
from sale.models import Invoice, Seating, Order, NotificationTable
from database.models import CompanyDetail, Branch, Credit, CreditHistory, Customer
from inventory.models import menu_item_signal, BillOfStock
from payment.models import VendorPayment

""" Invoice """


class InvoiceListByCompanyIdView(APIView):

    """ unused'"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            company = CompanyDetail.objects.get(pk=pk)
            branches = company.branch.all()
            invoices = []
            for branch in branches:
                branch_invoices = branch.invoice.all()
                for branch_invoice in branch_invoices:
                    invoices.append(branch_invoice)
            serializer = InvoiceListSerializer(invoices, many=True)
            return Response({'message': 'invoice list by company id',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        except:
            return Response({'message': 'company doesnot exist', 'status': status.HTTP_200_OK})


class InvoiceListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try:
            company, branch = token_helper(request)
            if branch is not None:
                obj = branch.invoice.all()
            else:
                obj = Invoice.objects.filter(branch__company=company)
            serializer = InvoiceListSerializer(obj, many=True)
            return Response({'message': 'Invoice list by branch',
                             'status': status.HTTP_200_OK,
                             'response': serializer.data})
        except Branch.DoesNotExist:
            return Response({'message': 'branch doesnot exist', 'status': status.HTTP_400_BAD_REQUEST})


class InvoiceDetailView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        try:
            company, branch = token_helper(request)
            obj = Invoice.objects.get(pk=pk)
            if obj.branch.company == company:
                serializer = InvoiceListSerializer(obj)
                return Response({'message': 'Invoice detail',
                                 'status': status.HTTP_200_OK,
                                 'response': serializer.data})
            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })

        except Exception as e:
            return Response({'message': "Invoice doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})


class InvoiceCreateView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        total_amount = 0
        try:
            seating_id = request.data.get('seating')
            seating = Seating.objects.get(id=seating_id)

            if seating.order.first() is not None:
                branch = seating.branch
                invoice = Invoice.objects.create(
                    seating=seating,
                    discount=0,
                    final_bill_amount=0,
                    misc_charge=0,
                    branch=branch,
                    paid_amount=0,
                )
                orders = seating.order.all()
                for order in orders:
                    invoice.order.add(order)
                    total_amount += order.final_price
                invoice.bill_amount = total_amount
                company = branch.company
                if company.vat_activated:
                    vat = company.vat_percentage
                else:
                    vat = 0
                vat_amount = total_amount * vat / 100
                if company.service_charge_activated:
                    service_charge = company.service_charge
                else:
                    service_charge = 0

                service_charge_amount = service_charge * total_amount / 100
                invoice.vat = vat
                invoice.vat_amount = vat_amount
                invoice.service_charge = service_charge
                invoice.service_charge_amount = service_charge_amount
                invoice.invoice_number = invoice.id
                invoice.save()
                serializer = InvoiceListSerializer(invoice)
                return Response({'message': 'invoice created successfully', 'status': status.HTTP_200_OK,
                                 'response': serializer.data})

            else:
                return Response({'message': 'already exists', 'status': status.HTTP_400_BAD_REQUEST})

        except:
            order_id = request.data.get('order')
            order = Order.objects.get(id=order_id)
            if order.itemline.first() is not None:
                branch = order.branch
                invoice = Invoice.objects.create(paid_amount=0)
                invoice.order.add(order)
                total_amount += order.final_price
                invoice.bill_amount = total_amount
                company = branch.company
                if company.vat_activated:
                    vat = company.vat_percentage
                else:
                    vat = 0
                vat_amount = total_amount * vat / 100
                if company.service_charge_activated:
                    service_charge = company.service_charge
                else:
                    service_charge = 0
                service_charge_amount = service_charge * total_amount / 100
                invoice.vat = vat
                invoice.vat_amount = vat_amount
                invoice.service_charge = service_charge
                invoice.service_charge_amount = service_charge_amount
                invoice.invoice_number = invoice.id
            invoice.save()
            menu_item_signal(invoice)


            serializer = InvoiceListSerializer(invoice)
            return Response({'message': 'invoice created successfully', 'status': status.HTTP_200_OK,
                                'response': serializer.data})
            # else:
            #     return Response({'message': 'already exists', 'status': status.HTTP_400_BAD_REQUEST})


class CustomerInvoiceHelperView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try:
            company, request = token_helper(request)
            customer = Customer.objects.filter(company=company)
            serializer = CustomerInvoiceHelperSerializer(customer, many=True)
            return Response({
                'message': 'customer info',
                'status': status.HTTP_200_OK,
                'response': serializer.data})

        except Customer.DoesNotExist:
            return Response({
                'message': 'customer doesnot exist',
                'status': status.HTTP_400_BAD_REQUEST
            })


class InvoiceUpdateView(APIView):
    """
    updates invoice and creates credit history accordingly
    """
    permission_classes = [IsAuthenticated, ]

    def patch(self, request, pk, *args, **kwargs):
        company, branch = token_helper(request)
        invoice = Invoice.objects.get(pk=pk)
        validated_data = request.data
        invoice.branch = validated_data.get('branch', invoice.branch)
        invoice.bill_date = validated_data.get('bill_date', invoice.bill_date)
        invoice.discount = Decimal(validated_data.get('discount', invoice.discount))
        invoice.final_bill_amount = Decimal(validated_data.get('final_bill_amount', invoice.final_bill_amount))
        invoice.paid_amount = Decimal(validated_data.get('paid_amount', invoice.paid_amount))
        invoice.return_amount = Decimal(validated_data.get('return_amount', invoice.return_amount))
        invoice.payment_mode = validated_data.get('payment_mode', invoice.payment_mode)
        invoice.available_amount = Decimal(validated_data.get('available_amount', invoice.available_amount))
        invoice.pay_from_debit = validated_data.get('pay_from_debit', invoice.pay_from_debit)

        if validated_data.get('customer') is not None or invoice.customer is not None:
            if validated_data.get('customer') is not None:
                customer_id = validated_data.get('customer')
            else:
                customer_id = invoice.customer.id
            invoice.customer = Customer.objects.get(id=customer_id)
            invoice.customer_name = invoice.customer.customer_name
        else:
            invoice.customer = None
        if validated_data.get('customer_name'):
            invoice.customer_name = validated_data.get('customer_name')
        invoice.invoice_status = 'paid'

        """ credit history calclulation """

        # we cannot allow scenario where:
        # customer invoice.paid_amount + credit_history.total_debit > invoice.final_bill_amount

        if invoice.customer is not None and invoice.customer.credit_privilege:
            customer = invoice.customer
            # if customer.credit_history is not None:
            try:
                credit_history = customer.credit_history
                if invoice.final_bill_amount > credit_history.total_debit + invoice.paid_amount:
                    invoice.pay_from_debit = False

            except:
                pass

                if invoice.pay_from_debit:
                    if credit_history.total_debit > 0.0:
                        if credit_history.total_debit >= invoice.final_bill_amount:
                            transaction_amount = invoice.final_bill_amount
                            invoice.paid_amount = 0
                            invoice.invoice_status = "paid"
                        else:
                            transaction_amount = credit_history.total_debit
                            invoice.invoice_status = "paid"

                        credit = Credit.objects.create(
                            credit_status='credited',
                            transaction_amount=transaction_amount,
                            credit_history=credit_history,
                            customer=customer,
                            invoice=invoice,
                            remarks="from invoice #{}.".format(
                                invoice.invoice_number)
                        )
                        credit.save()

            if invoice.paid_amount == invoice.final_bill_amount + invoice.return_amount:
                invoice.invoice_status = 'paid'

            elif invoice.paid_amount > invoice.final_bill_amount + invoice.return_amount:
                if invoice.payment_mode == 'credit':
                    if invoice.customer is not None and invoice.customer.credit_privilege:
                        credit_status = 'debited'
                        # invoice.invoice_status = 'paid'
                        transaction_amount = invoice.paid_amount - invoice.final_bill_amount - invoice.return_amount

                        try:
                            credit_history = invoice.customer.credit_history

                        except:
                            credit_history = CreditHistory.objects.create(
                                customer=invoice.customer)
                            credit_history.save()

                        try:
                            credit = Credit.objects.get(invoice=invoice)
                            credit.transaction_amount = transaction_amount
                            credit.credit_status = credit_status

                        except:
                            credit = Credit.objects.create(
                                credit_status=credit_status,
                                transaction_amount=transaction_amount,
                                credit_history=credit_history,
                                customer=invoice.customer,
                                invoice=invoice,
                                remarks="from invoice #{}".format(
                                    invoice.invoice_number)
                            )
                        credit.save()
                    else:
                        raise ValueError('paid amount cannot be more than final bill amount')

                else:
                    raise ValueError(
                        ' paid_amount cannot be more than sum of final bill amount and return amount ')

            elif invoice.paid_amount < invoice.final_bill_amount + invoice.return_amount:
                if invoice.payment_mode == 'credit':
                    if invoice.customer is not None and invoice.customer.credit_privilege:
                        credit_status = 'credited'
                        transaction_amount = invoice.final_bill_amount - invoice.paid_amount

                        try:
                            credit_history = invoice.customer.credit_history

                        except:
                            credit_history = CreditHistory.objects.create(
                                customer=invoice.customer)
                            credit_history.save()

                        try:
                            credit = Credit.objects.get(invoice=invoice)
                            credit.transaction_amount = transaction_amount
                            credit.credit_status = credit_status

                        except:
                            credit = Credit.objects.create(
                                credit_status=credit_status,
                                transaction_amount=transaction_amount,
                                credit_history=credit_history,
                                customer=invoice.customer,
                                invoice=invoice,
                                remarks="from invoice #{}".format(
                                    invoice.invoice_number)
                            )
                        credit.save()
                    else:
                        raise ValueError('paid amount cannot be less than final bill amount ')

                else:
                    raise ValueError(
                        'paid amount cannot be less than final bill amount')

        if invoice.branch.company == company:
            invoice.save()
            menu_item_signal(invoice)
            seating_id = invoice.seating.id
            seating = Seating.objects.get(id=seating_id)

            """ seating cleaner """
            seating.order.clear()
            seating.customer = None
            seating.waiter = None
            seating.seating_status = 'available'
            seating.merge_reference = None
            seating.reservation = None
            seating.save()
            """ end """

            """ Notification table delete """
            notifications = NotificationTable.objects.filter(
                seating_id=seating_id)
            for notification in notifications:
                notification.delete()
            """ end """

            return Response({
                'message': "Invoice updated succesfully",
                'status': status.HTTP_204_NO_CONTENT,
            })
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })

    def put(self, request, pk):
        company, branch = token_helper(request)
        invoice = Invoice.objects.get(pk=pk)
        if invoice.branch == branch:
            invoice.remark = request.data.get('remark')
            invoice.invoice_status='canceled'
            invoice.save()
            return Response({
                'message': 'remarks added',
                'status': status.HTTP_200_OK
            })
        else:
            return Response({
                'message': 'Unauthorized',
                'status': status.HTTP_401_UNAUTHORIZED
            })


class InvoiceDeleteView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk):
        try:
            company, branch = token_helper(request)
            obj = Invoice.objects.get(pk=pk)
            if obj.branch == branch:
                obj.invoice_status = 'canceled'
                print(obj.invoice_status)
                obj.remark = request.data.get('remark', 'canceled')
                print(obj.remark)
                obj.save()
                return Response({'message': 'Invoice successfully canceld',
                                 'status': status.HTTP_200_OK})

            else:
                return Response({
                    'message': 'Unauthorized',
                    'status': status.HTTP_401_UNAUTHORIZED
                })
        except Exception as e:
            return Response({'message': "Invoice doesn't exist", 'status': status.HTTP_400_BAD_REQUEST})



class VendorPaymentView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        company, branch = token_helper(request)
        if branch is not None:
            payment = VendorPayment.objects.filter(branch=branch)
        else:
            payment = VendorPayment.objects.filter(branch__company = company)
        serializer = VendorPaymentListSerializer(payment, many = True)
        return Response({"message": "success", "status": status.HTTP_200_OK, "response":serializer.data})


class VendorPaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]

    def patch(self, request, pk):
        company, branch = token_helper(request)
        vendor_payment = VendorPayment.objects.get(pk=pk)
        if vendor_payment.branch.company == company:
            serializer = VendorPaymentUpdateSerializer(vendor_payment, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                if serializer.data['payment_status'] == "paid":
                    bill = BillOfStock.objects.get(branch = serializer.data['branch'], id = serializer.data['bill_of_stock'])
                    if bill:
                        bill.payment_status = serializer.data["payment_status"]
                        bill.save()
                else:
                    return Response({'message': 'payment status is unpaid please pay your due amount'})
                return Response({"message":"success", "status":status.HTTP_200_OK, "response":serializer.data})
            return Response({"message":"error", "status":status.HTTP_400_BAD_REQUEST, "response":serializer.errors})
