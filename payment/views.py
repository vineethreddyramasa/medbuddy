import braintree
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import weasyprint
from io import BytesIO
from twilio.rest import Client

def payment_process(request):
	order_id = request.session.get('order_id')
	order = get_object_or_404(Order, id=order_id)

	if request.method == 'POST':
		# retrieve nonce
		nonce = request.POST.get('payment_method_nonce', None)
		# create and submit transaction
		result = braintree.Transaction.sale({
			'amount': '{:.2f}'.format(order.get_total_cost()),
			'payment_method_nonce': nonce,
			'options': {
			'submit_for_settlement': True
			}
		})
		if result.is_success:
			# mark the order as paid
			order.paid = True
			# store the unique transaction id
			order.braintree_id = result.transaction.id
			order.save()
			# create invoice e-mail
			subject = 'My Shop - Invoice no. {}'.format(order.id)
			message = 'Please, find attached the invoice for your recent purchase.'
			email = EmailMessage(subject,
								message,
								'admin@medbuddyshop.com',
								[order.email])
			# generate PDF
			html = render_to_string('orders/order/pdf.html', {'order':order})
			out = BytesIO()
			stylesheets=[weasyprint.CSS(settings.STATIC_ROOT +'css/pdf.css')]
			weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
			# attach PDF file
			email.attach('order_{}.pdf'.format(order.id),
				out.getvalue(),
				'application/pdf')
			# send e-mail
			email.send()

			# send sms
			# Your Account SID from twilio.com/console
			account_sid = "AC1cac4d02cc38ebe54d55d730ca00703c"
			# Your Auth Token from twilio.com/console
			auth_token = "423946a57f6b878f341abe7d66b3fe2f"

			client = Client(account_sid, auth_token)

			message = client.messages.create(
				to="+14027066443",
				from_="+117122484584",
				body="Thank you {} {}, Your order {} has been placed successfully and will be delivered to {}, {}, {}".format(order.first_name,order.last_name,order.id,order.address,order.city,order.postal_code)
			)
			print(message.sid)

			return redirect('payment:done')
		else:
			return redirect('payment:canceled')
	else:
		# generate token
		client_token = braintree.ClientToken.generate()
		return render(request,
			'payment/process.html',
			{'order': order,
			'client_token': client_token})

def payment_done(request):
	return render(request, 'payment/done.html')

def payment_canceled(request):
	return render(request, 'payment/canceled.html')

