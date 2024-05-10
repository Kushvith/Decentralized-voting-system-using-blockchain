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
        <div class="card mb-4 show_ele">
          <div class="card-header pb-0 d-flex">
            <h6>Show Elections</h6>
            <button class="ms-auto btn btn-primary btn-sm create_ele_btn">create new Eletion</button>
          </div>
          <div class="card-body px-0 pt-0 pb-2">
            <div class="table-responsive p-0">
              <table class="table align-items-center mb-0">
                <thead>
                  <tr>
                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">name</th>
                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">election_time
                    </th>
                    <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">party
                    </th>
                    <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">status
                    </th>
                    <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                      created_time</th>
                    <th class="text-secondary opacity-7">Action</th>
                  </tr>
                </thead>
                <tbody id="sched_ele">

                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div class="card mb-4 show_ele">
          <div class="card-header pb-0 d-flex">
            <h6>Results</h6>
          </div>
          <div class="card-body px-0 pt-0 pb-2">
            <div class="table-responsive p-0">
              <table class="table align-items-center mb-0">
                <thead class="text-center">
                  <tr>
                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Election Name</th>
                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">election date
                    </th>
                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">total parties
                    </th>
                    <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">status
                    </th>
                  </tr>
                </thead>
                <tbody id="ele_res" class="text-center">

                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div class="card mb-4 create_ele">
          <div class="card-header pb-0 d-flex">
            <h6>Schedule Elections</h6>
            <button class="ms-auto btn btn-primary btn-sm view_ele">view</button>
          </div>
          <div class="card-body px-0 pt-0 pb-2">
            <div class="d-flex justify-content-between align-items-center ms-5">
              <form id="create_eleform">
                <div class="form-group">
                  <label for="name">Election Name</label>
                  <input type="text" id="name" name="election_name" class="form-control ms-3 outline-none"
                    placeholder="Election name">
                </div>
                <div class="form-group">
                  <label for="name">Time</label>
                  <input type="date" id="time" name="time" class="form-control ms-3 outline-none"
                    placeholder="Election name">
                </div>
                <div class="form-group d-flex align-items-center justify-content-center">
                  <button type="button" class="btn btn-success create_election">Create Election</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>


  <div class="modal fade" id="exampleModal1" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
    aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Result Analysis</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th>party_name</th>
                  <th>Vote_counts</th>
                </tr>
              </thead>
              <tbody id="res_anl">

              </tbody>
            </table>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>

        </div>
      </div>
    </div>
  </div>
  <!-- Modal -->
  <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
    aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Add Parties</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="party_data">

          </div>
          <div class="select_party">
            <div class="table-responsive p-0">
              <table class="table align-items-center mb-0">
                <thead>
                  <tr>
                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Candidate name
                    </th>
                    <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Party
                      name
                    </th>
                    <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Age
                    </th>
                    <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Image
                    </th>
                    <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder ">Action</th>
                  </tr>
                </thead>
                <tbody class="mr-2">

                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>

        </div>
      </div>
    </div>
  </div>
  <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
    integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
    crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js"
    integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
    crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js"
    integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
    crossorigin="anonymous"></script>
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
  <script>
    $('.create_ele').hide()
    $('.create_ele_btn').click(function () {
      $('.show_ele').hide()
      $('.create_ele').show()
    })
    $('.view_ele').click(function () {
      $('.show_ele').show()
      $('.create_ele').hide()
    })

    $(document).ready(function () {
      fetch_results()
      
      function fetch_results(){
        $.ajax({
          method:"GET",
          url:"../php/election.php",
          data:{"fetch_res":"fetch_res"},
          success:function(data){
            $('#ele_res').html(data)
          }
        })
      }
      $(document).on('click','#view',function(){
        id = $(this).data('id')
        $.ajax({
          method:"post",
          url:"../php/election.php",
          data:{"res_anl":id},
          success:function(data){
            $('#res_anl').html(data)
          }
        })
      })
      function fetch_checklist(id) {
        $.ajax({
          method: "POST",
          url: "../php/party.php",
          data: { "party_candidate": "party_candidate", "par_id": id },
          success: function (data) {
            parse = JSON.parse(data)
            console.log(parse)
            $('.party_data').html('')
            for (let index = 0; index < parse.length; index++) {
              $('.party_data').append(
                "<div class='form-check'><input id='checkbox' class='form-check-input' type='checkbox' value='" + parse[index][0] + "'/><label class='form-check-label'>" + parse[index][1] + " - " + parse[index][2] + "</label></div>"
              )

            }
            $('.modal-footer').html('')
            $('.modal-footer').append(' <button type="button" class="btn btn-primary" id="save_changes" data-id=' + id + '>Save changes</button>')
            fetch_party_election(id)
          },
          error: (xhr, status, error) => {
            console.log(JSON.parse(xhr.responseText).message)
          }
        })
      }
      $(document).on('click', '#delete', function () {
        var id = $(this).data('id')
        $.ajax({
          url: "../php/election.php",
          method: "POST",
          data: { "delete_id": id },
          success: function (data) {
            fetch()
          }
        })
      })
      $(document).on('click', '#complete', function () {
        var currentUrl = window.location.href;
        var urlObject = new URL(currentUrl);
        urlObject.protocol = "https:";
        urlObject.port = "5000";
        urlObject.pathname = "/fetch_results";
        var newUrl = urlObject.href;
        $.ajax({
          url:newUrl,
          method:"GET",
          dataType: "jsonp",
          success:function(data){
            (data.message)
            fetch()
          }
        })
      })
      $(document).on("click", '.party-btn', function () {
        var id = $(this).data("id")
        fetch_checklist(id)
      })
      $(document).on('click', '#delete_modal', function () {
        ele_id = $(this).data('ele')
        party_id = $(this).data('id')
        $.ajax({
          method: "post",
          url: "../php/party.php",
          data: { "election_id": ele_id, "party_id": party_id },
          success: function (data) {
            fetch_checklist(ele_id)
            fetch_party_election(ele_id)
          }
        })
      })
      $(document).on('click', '#save_changes', function () {
        id = $("#save_changes").data('id')
        var checkeditem = []
        $('#checkbox:checked').each(function () {
          var value = $(this).val()
          checkeditem.push(value)
        })
        $.ajax({
          method: "post",
          url: "../php/party.php",
          data: { "ele_id": id, "par_up_id": checkeditem },
          success: function (data) {
            if (data == 1) {
              fetch_checklist(id)
              fetch_party_election(id)
            }
          }

        })
      })
      function fetch_party_election(id) {
        $.ajax({
          method: "POST",
          url: "../php/party.php",
          data: { "party_ele_table": id },
          success: function (data) {
            $('.select_party tbody').html(data)
          },
          error: (xhr, status, error) => {
            console.log(JSON.parse(xhr.responseText).message)
          }
        })
      }
      function fetch() {
        $.ajax({
          method: 'GET',
          url: "../php/election.php",
          data: { "table": "table_data" },
          success: function (data) {
            $('#sched_ele').html(data)
          },
          error: (xhr, status, error) => {
            console.log(JSON.parse(xhr.responseText).message)
          }
        })
      }
      fetch()
      $('.create_election').click(function () {
        if ($('#name').val() == "" || $('#time').val() == "") {
          ("All feilds required")
        } else {
          $.ajax({
            method: 'POST',
            url: "../php/election.php",
            data: $('#create_eleform').serialize(),
            success: function (data) {
              if (data == true) {
                $('#create_eleform').trigger("reset")
                $('.show_ele').show()
                fetch()
              }
            },
            error: (xhr, status, error) => {
              console.log(JSON.parse(xhr.responseText).message)
            }

          })
        }
      })

    })
  </script>
  <!-- Github buttons -->
  <script async defer src="https://buttons.github.io/buttons.js"></script>
  <!-- Control Center for Soft Dashboard: parallax effects, scripts for the example pages etc -->
  <script src="../assets/js/soft-ui-dashboard.min.js?v=1.0.7"></script>
</body>

</html>