app = angular.module 'js.darg.app.index', ['js.darg.api',]

app.controller 'IndexController', ['$scope', '$http', 'Invitee', ($scope, $http, Invitee) ->
    $scope.show_add_invitee = true
    $scope.newInvitee = new Invitee()
    $scope.errors = []

    $scope.add_invitee = ->
        $scope.newInvitee.$save().then (result) ->
            $scope.show_add_invitee = false
            # track form open
            if !_.isUndefined(window.ga)
                ga 'send', 'event', 'click', 'save_invitee_email'
        .then ->
            # Reset our editor to a new blank post
            $scope.newInvitee = new Invitee()
        .then ->
            # Clear any errors
            $scope.errors = null
        , (rejection) ->
            $scope.errors = rejection.data
]
