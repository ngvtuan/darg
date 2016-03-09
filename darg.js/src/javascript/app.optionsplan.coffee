app = angular.module 'js.darg.app.optionplan', ['js.darg.api', 'xeditable', 'ngFileUpload']

app.controller 'OptionPlanController', ['$scope', '$http', 'OptionPlan', 'Upload', '$timeout', ($scope, $http, OptionPlan, Upload, $timeout) ->

    $scope.file = null
    $scope.pdf_upload_success = false
    $scope.pdf_upload_errors = false
    $scope.loading = false

    $http.get('/services/rest/optionplan/' + optionplan_id).then (result) ->
        $scope.optionplan = new OptionPlan(result.data)
        $scope.optionplan.board_approved_at = $scope.optionplan.board_approved_at

    $http.get('/services/rest/security').then (result) ->
        $scope.securities = result.data.results

    $scope.$watch 'files', ->
      $scope.upload $scope.files
      return
    $scope.$watch 'file', ->
      if $scope.file != null
        $scope.files = [ $scope.file ]
      return
    $scope.log = ''

    $scope.upload = (files) ->
      if files and files.length
        $scope.loading = true
        i = 0
        while i < files.length
          file = files[i]
          if !file.$error
            # prepare data
            payload = $scope.optionplan
            payload.pdf_file = file
            Upload.upload(
              url: '/services/rest/optionplan/'+optionplan_id+'/upload'
              data: payload
              objectKey: '.k').then ((response) ->
                $timeout ->
                  $scope.optionplan = response.data
                  $scope.pdf_upload_success = true
                  $scope.pdf_upload_errors = false
                  return
                $timeout(() ->
                  $scope.pdf_upload_success = false
                , 3000)
              ), ((response) ->
                $timeout ->
                  $scope.pdf_upload_errors = response.data
              ), (evt) ->
                return
              $scope.loading = false
              return
]

app.run (editableOptions) ->
  editableOptions.theme = 'bs3'
  # bootstrap3 theme. Can be also 'bs2', 'default'
  return
