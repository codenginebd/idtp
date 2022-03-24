function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
              }
          }
      }
      return cookieValue;
  }

  window.get_csrf_token = () =>  getCookie("csrftoken");

  function ajax_call(type, url, data) {
    let promise = new Promise((resolve, reject) => {
        $.ajax({
          type: type,
          url: url,
          dataType: "json",
          data: data,
          beforeSend: function(xhr){xhr.setRequestHeader('X-CSRFToken', window.get_csrf_token());},
          xhrFields: {
              withCredentials: true
          },
          success: function (data) {
              console.log(data);
              resolve(data);
          },
          error: function (jqxhr, status, error) {
            reject(jqxhr, status, error);
          }
      });
    });
    return promise;
  }


$(document).ready(function () {

  $("#idBtnRegNewUser").click(function (e) {
        e.preventDefault();
        $("#idDialogUserReg").modal("show");
        return false;
  });

  $("#idBtnTrnsferFund").click(function (e) {
        e.preventDefault();
        $("#idDialogFundTransfer").modal("show");
        return false;
  });

  $("#idBtnReqRTP").click(function (e) {
        e.preventDefault();
        $("#idDialogRTP").modal("show");
        return false;
  });

  $("#idBtnSubmitReg").click(function (e) {
          e.preventDefault();
          var _data = $("#idFormUserReg").serialize();
          ajax_call("POST", "/submit-user-registration/", _data).then(function (data) {
              console.log("Success");
              if(data.status === "SUCCESS")
              {
                alert("Registration successful");
              }
              else {
                  alert("Registration Failed. Reason: " + data.message);
              }
              //window.location.href="/";
              return false;
          }).then(function (err) {
              alert("Registration Failed");
              return false;
          });
          return false;
  });

  $("#idBtnTransferFund").click(function (e) {
          e.preventDefault();
          var _data = $("#idFormFundTransfer").serialize();
          ajax_call("POST", "/submit-fund-transfer/", _data).then(function (data) {
              console.log("Success");
              if(data.status === "SUCCESS") {
                  alert("Fund Transfer Successful");
              }
              else {
                  alert("Fund Transfer Failed. Reason: " + data.message);
              }
              //window.location.href="/";
              return false;
          }).catch(function (err) {
              alert("Fund Transfer Failed");
              return false;
          });
          return false;
  });

  $("#idBtnReqRTPSubmit").click(function (e) {
          e.preventDefault();
          var _data = $("#idFormReqRTPForm").serialize();
          ajax_call("POST", "/submit-rtp/", _data).then(function (data) {
              console.log("Success");
              alert("RTP Request Successful");
              //window.location.href="/";
              return false;
          }).catch(function (err) {
              alert("RTP Request Failed");
              return false;
          });
          return false;
  });

  $(".rtp-decline").click(function (e) {
      e.preventDefault();
      var _senderVid = $(this).data("sender-vid");
      var _receiverVid = $(this).data("receiver-vid");
      var _rtpId = $(this).data("req-id");

      var _data = {
            "sender_vid": _senderVid,
            "receiver_vid": _receiverVid,
            "rtp_id": _rtpId
      };

      ajax_call("POST", "/decline-rtp/", _data).then(function (data) {
              console.log("Success");
              alert("RTP Decline Successful");
              //window.location.href="/";
              return false;
          }).catch(function (err) {
              alert("RTP Decline Failed");
              return false;
          });

      return false;
  });

  $(".rtp-accept").click(function (e) {
      e.preventDefault();
      e.preventDefault();
      var _senderVid = $(this).data("sender-vid");
      var _receiverVid = $(this).data("receiver-vid");
      var _rtpId = $(this).data("req-id");
      var _amount = $(this).data("amount");
      var _purpose = $(this).data("ref");

      $("#idHiddenRefNoAcceptRTP").val(_rtpId);
      $("#idDialogRTPAccept").find("input[name=sender_vid]").val(_receiverVid);
      $("#idDialogRTPAccept").find("input[name=receiver_vid]").val(_senderVid);
      $("#idDialogRTPAccept").find("input[name=amount]").val(_amount);
      $("#idDialogRTPAccept").find("input[name=purpose]").val(_purpose);

      $("#idDialogRTPAccept").modal("show");

      return false;
  });

  $("#idBtnReqRTPAcceptSubmit").click(function (e) {
          e.preventDefault();
          var _data = $("#idFormAcceptRTPForm").serialize();
          ajax_call("POST", "/approve-rtp/", _data).then(function (data) {
              console.log("Success");
              if(data.status === "SUCCESS") {
                  alert("RTP Approved Successful");
              }
              else {
                  alert("RTP Approve Failed. Reason: " + data.message);
              }
              //window.location.href="/";
              return false;
          }).catch(function (err) {
              alert("RTP could not be approved");
              return false;
          });
          return false;
  });

  $(".view-user-tnx").click(function (e) {
      e.preventDefault();
      var _userVid = $(this).data("vid");
      $("#idHiddenTnxUserVid").val(_userVid);
      $("#idDialogViewUserTnxHistory").modal("show");
      return false;
  });

  $("#idFormViewUserTnxHistoryFormSubmit").click(function (e) {
      e.preventDefault();
      window.location.href = "/GetDailyTransactions/?vid=" + $("#idHiddenTnxUserVid").val() + "&idtp_pin=" + $("#idViewUserTnxIDTPPin").val();
  });
});