(function () {
  'use strict';

  // Declare app level module which depends on views, and components
  angular.module('authentiq-angular', [])
    .provider('authentiq', authentiqProvider)
    .run(setUserState)
    .run(listenEventHandlers);

  /**
   * @name authentiqProvider
   * @desc loads the Authentiq snippet inside an angular module
   *       and registers it as an angular provider
   */
  function authentiqProvider() {
    this.$get = function () {
      return window.authentiq;
    };
  }

  /**
   * @name setUserState
   * @desc check if user is logged in or not when app loads
   */
  function setUserState($rootScope, authentiq) {
    // check if user is logged in
    $rootScope.loggedIn = authentiq.Provider.isSignedIn();

    // load the user profile
    $rootScope.profile = authentiq.Provider.profile();
  }

  /**
   * @name listenEventHandlers
   * @desc subscribe to authentiq events
   */
  function listenEventHandlers($rootScope, $log, authentiq) {
    
    // listen for `profile` event from Authentiq snippet,
    // which is being fired on successful login
    authentiq.subscribe('profile', function(profile) {
      // update user state and profile in UI
      $rootScope.loggedIn = true;
      $rootScope.profile = profile;
      $rootScope.$apply();
    });

    // listen for `concluded` event from Authentiq snippet,
    // which is being fired on logout
    authentiq.subscribe('concluded', function() {
      // update user state and profile in UI
      $rootScope.loggedIn = false;
      $rootScope.profile = {};
      $rootScope.$apply();
    });

    // listen for `error` event from Authentiq snippet, used for logging
    authentiq.subscribe('error', function(error) {
      $log.warn(error);
    });
  }
})();