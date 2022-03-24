from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from pim.views.approve_rtp_view import ApproveRTPView
from pim.views.audit_log_view import AuditLogView
from pim.views.create_rtp_request_view import CreateRTPRequestView
from pim.views.decline_rtp_view import DeclineRTPView
from pim.views.get_account_balance_view import GetAccountBalanceView
from pim.views.get_daily_transaction_view import GetDailyTransactionsView
from pim.views.get_rtp_list_received_view import GetRTPListReceivedView
from pim.views.get_rtp_list_sent_view import GetRTPListSentView
from pim.views.home_view import HomeView
from pim.views.initiate_fund_transfer_view import InitiateFundTransferView
from pim.views.process_fund_transfer_view import ProcessFundTransferRequestView
from pim.views.process_rtp_decline_response_view import ProcessRTPDeclineResponseView
from pim.views.process_rtp_request_view import ProcessRTPRequestView
from pim.views.scb_accounts_view import SCBAccountsView
from pim.views.submit_fund_transfer_view import SubmitFundTransferView
from pim.views.submit_rtp_view import SubmitRTPView
from pim.views.submit_user_reg_view import SubmitUserRegView
from pim.views.validate_fi_user_view import ValidateFIUserView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home_view'),
    url(r'^ProcessFundTransferRequest$', csrf_exempt(ProcessFundTransferRequestView.as_view()), name='process_fund_transfer_view'),
    url(r'^GetAccountBalance$', GetAccountBalanceView.as_view(), name='get_account_balance_view'),
    url(r'^CreateRTPRequest$', CreateRTPRequestView.as_view(), name='create_rtp_request_view'),
    url(r'^ProcessRTPRequest$', ProcessRTPRequestView.as_view(), name='process_rtp_request_view'),
    url(r'^ProcessRTPDeclinedResponse$', ProcessRTPDeclineResponseView.as_view(), name='process_rtp_decline_response_view'),
    url(r'^InitiateFundTransfer$', InitiateFundTransferView.as_view(), name='initiate_fund_transfer_view'),
    url(r'^ValidateFIUser$', ValidateFIUserView.as_view(), name='validate_fi_user_view'),
    url(r'^GetDailyTransactions/$', GetDailyTransactionsView.as_view(), name='get_daily_transaction_view'),
    url(r'^get-rtp-list-sent/$', GetRTPListSentView.as_view(), name='get_rtp_list_sent_view'),
    url(r'^get-rtp-list-received/$', GetRTPListReceivedView.as_view(), name='get_rtp_list_received_view'),
    url(r'^submit-user-registration/$', SubmitUserRegView.as_view(), name='submit_user_reg_view'),
    url(r'^submit-fund-transfer/$', SubmitFundTransferView.as_view(), name='submit_fund_transfer_view'),
    url(r'^submit-rtp/$', SubmitRTPView.as_view(), name='submit_rtp_view'),
    url(r'^approve-rtp/$', ApproveRTPView.as_view(), name='approve_rtp_view'),
    url(r'^decline-rtp/$', DeclineRTPView.as_view(), name='decline_rtp_view'),
    url(r'^audit-log/$', AuditLogView.as_view(), name='audit_log_view'),
    url(r'^scb-accounts/$', SCBAccountsView.as_view(), name='scb_accounts_view'),

]
