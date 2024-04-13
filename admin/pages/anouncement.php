
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link rel="apple-touch-icon" sizes="76x76" href="../assets/img/apple-icon.png">
  <link rel="icon" type="image/png" href="../assets/img/favicon.png">
  <title>
   Staff Dashboard
  </title>
  <!--     Fonts and icons     -->
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700" rel="stylesheet" />
  <!-- Nucleo Icons -->
  <link href="../assets/css/nucleo-icons.css" rel="stylesheet" />
  <link href="../assets/css/nucleo-svg.css" rel="stylesheet" />
  <!-- Font Awesome Icons -->
  <script src="https://kit.fontawesome.com/42d5adcbca.js" crossorigin="anonymous"></script>
  <link href="../assets/css/nucleo-svg.css" rel="stylesheet" />
  <!-- CSS Files -->
  <link id="pagestyle" href="../assets/css/soft-ui-dashboard.css?v=1.0.7" rel="stylesheet" />
  <!-- Nepcha Analytics (nepcha.com) -->
  <!-- Nepcha is a easy-to-use web analytics. No cookies and fully compliant with GDPR, CCPA and PECR. -->
  <script defer data-site="YOUR_DOMAIN_HERE" src="https://api.nepcha.com/js/nepcha-analytics.js"></script>
</head>

<body class="g-sidenav-show  bg-gray-100">
<?php  
  include('../php/side_top.php');
?>
    <!-- End Navbar -->
    <div class="container-fluid py-4">
      <div class="row">
        <div class="col-12">
          <div class="card mb-4">
            <div class="card-header pb-0 d-flex">
              <h6>Announcements</h6>
            </div>
            <div class="card-body px-4 pt-0 pb-2" id="view_btn">
              <div class="row" id="view">
                
              </div>
            </div>
            <div class="card-body px-0 pt-0 pb-2" id="create">
              <div class="row">
                  <div class="col-md-6 offset-md-3">
                      <div class="form-group">
                        <label >Announcement</label>
                        <textarea id="announce_text" class="form-control" cols="30" rows="3" placeholder="create your Announcements here..."></textarea>
                      </div>
                      <button class="btn btn-primary" id="create_an">Create</button>
                  </div>
              </div>
            </div>
          </div>
        </div>
      </div>
 
    </div>
  </main>


  <!--   Core JS Files   -->
  <script src="../assets/js/core/popper.min.js"></script>
  <script src="../assets/js/core/bootstrap.min.js"></script>
  <script src="../assets/js/plugins/perfect-scrollbar.min.js"></script>
  <script src="../assets/js/plugins/smooth-scrollbar.min.js"></script>
  <script>
    var win = navigator.platform.indexOf('Win') > -1;
    if (win && document.querySelector('#sidenav-scrollbar')) {
      var options = {
        damping: '0.5'
      }
      Scrollbar.init(document.querySelector('#sidenav-scrollbar'), options);
    }
  </script>
  <!-- Github buttons -->
  <script async defer src="https://buttons.github.io/buttons.js"></script>
  <!-- Control Center for Soft Dashboard: parallax effects, scripts for the example pages etc -->
  <script src="../assets/js/soft-ui-dashboard.min.js?v=1.0.7"></script>
</body>
<script>
  $(document).ready(function(){
    fetch()
    $('#create_an').click(function(){
      an_val = $('#announce_text').val()
      if(an_val== ""){
        alert("announcement feild is required")
      }else{
        $.ajax({
          method:"POST",
          url:"../php/contact.php",
          data:{"announce_text":an_val},
          success:function(data){
            $('#announce_text').val("")
            fetch()
          }
        })
      }
    })
    $(document).on('click','#delete',function(){
      id = $(this).data('id')
      $.ajax({
        method:"POST",
        url:"../php/contact.php",
        data:{id},
        success:function(data){
          fetch()
        }
      })
    })
    function fetch(){
      $.ajax({
        method:"GET",
        url:"../php/contact.php",
        data:{"ann_data":"ann_data"},
        success:function(data){
          $('#view').html(data)
        }
      })
    }
  })
</script>
</html>