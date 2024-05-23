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
  include ('../php/side_top.php');
  ?>
  <!-- End Navbar -->
  <div class="container-fluid py-4">
    <div class="row">
      <div class="col-12">
        <div class="card mb-4 table_view">
          <div class="card-header pb-0 d-flex">
            <h6>Party table</h6>
            <button class="btn btn-primary btn-sm ms-auto" id="create-btn">Create new Party</button>
          </div>
          <div class="card-body px-0 pt-0 pb-2">
            <div class="table-responsive p-0">
              <table class="table align-items-center mb-0">
                <thead>
                  <tr>
                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Candidate name</th>
                    <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Party name
                    </th>
                    <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Age
                    </th>
                    <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Image</th>
                    <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder ">Action</th>
                  </tr>
                </thead>
                <tbody class="mr-2">

                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div class="card mb-4 form_party">
          <div class="card-header pb-0 d-flex">
            <h6>Create Party</h6>
            <button class="btn btn-primary btn-sm ms-auto" id="view-btn">View Party</button>
          </div>
          <div class="card-body px-0 pt-0 pb-2 row">
            <form class="ms-auto me-auto col-md-6 offset-md-3 ">
              <div class="form-group">
                <label for="candidate_name">Candidate Name</label>
                <input type="text" name="candidate_name" id="candidate_name" class="form-control w-50 ms-3"
                  placeholder="candidate name" />
              </div>
              <div class="form-group">
                <label for="party_name">party Name</label>
                <input type="text" name="party_name" id="party_name" class="form-control w-50 ms-3"
                  placeholder="party name" />
              </div>
              <div class="form-group">
                <label for="age">Age</label>
                <input type="number" name="age" id="age" class="form-control w-50 ms-3" placeholder="Age" min="18"
                  max="100">
              </div>
              <div class="form-group">
                <label for="Logo">Party Logo</label>
                <input type="file" name="party_logo" id="Logo" class="form-control w-50 ms-3" placeholder="Age"
                  accept="image/*">
              </div>
              <div id="loader" style="display: none;">
    <div class="spinner-border text-primary" role="status">
        <span class="sr-only">Loading...</span>
    </div>
</div>
              <button class="btn bg-success p-3 text-center offset-md-3" id="create_party_form">Create Party</button>
            </form>
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
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js"
    integrity="sha512-v2CJ7UaYy4JwqLDIrZUI/4hqeoQieOmAZNXBeQyjo21dadnwR+8ZaIJVT8EE2iyI61OV8e6M8PP2/4hpQINQ/g=="
    crossorigin="anonymous" referrerpolicy="no-referrer"></script>
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
  <script>
    $(document).ready(function () {
      $('.form_party').hide()
      $('#create-btn').click(function () {
        $('.table_view').hide()
        $('.form_party').show()
      })
      $('#view-btn').click(function () {
        $('.table_view').show()
        $('.form_party').hide()
      })
      function fetch(){
      $.ajax({
        method: 'GET',
        url: "../php/party.php",
        data: { "table": "table_data" },
        success: function (data) {
          $('tbody').html(data)
        }
      })
    }
    fetch()
      $('#create_party_form').click(function (e) {
        $('#loader').show();
        $(this).hide()
        e.preventDefault()
        img = $('#Logo').val()
        age = $('#age').val()
        party = $('#party_name').val()
        candidate = $('#candidate_name').val()
        if (img == "" || age == "" || party == "" || candidate == "") {
          alert("all feilds required")
        }
        else if (parseInt(age) < 18) {
          alert("age should be above 18")
        }
        else {
          var formdata = new FormData()
          var files = $('#Logo')[0].files;
          formdata.append("fileimg", files[0])
          formdata.append('age', age)
          formdata.append('party', party)
          formdata.append('candidate', candidate)
          console.log(formdata)
          $.ajax({
            url: "../php/party.php",
            method: "post",
            data: formdata,
            contentType: false,
            processData: false,

            success: (data)=>{
              alert("party created successfully")
              $('#loader').hide();
        $("#create_party_form").show()
              img = $('#Logo').val("")
        age = $('#age').val("")
        party = $('#party_name').val("")
        candidate = $('#candidate_name').val("")
              fetch()
            },
            error: (xhr, status, error) => {
              console.log(JSON.parse(xhr.responseText).message)
            }
          })

        }
      })
      $(document).on('click','#delete',function() {
        id = $(this).data('id')
        $.ajax({
          url: "../php/party.php",
          method:'POST',
          data:{"id":id},
          success:function(data){
            if(data == 1){
              fetch();
            }
            else{
              alert("Some error occured")
              fetch();
            }
          }
        })
      })
    })
  </script>
</body>

</html>