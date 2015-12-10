(function(){
    angular.module('recipehub')
        .controller('RecipeController', ['RecipeService', '$scope', '$routeParams', 'CommentService', 'RatingService', '$mdDialog', function recipeController($recipeService, $scope, $routeParams, $commentService, $ratingService, $mdDialog) {

            var recipeId = $routeParams.id;
            var scope = $scope;
            $scope.forks = [];

            if ($routeParams.fork) {
                forkAlert();
            }

            $recipeService.getForks(recipeId)
                .then(function (response) {
                    $scope.forks = JSON.parse(response.data);
                });

            $recipeService.getVersions(recipeId)
                .then(function (response) {
                    $scope.versions = JSON.parse(response.data);
                });

            $recipeService.getRecipe(recipeId, $routeParams.version_id)
                .then(function (response) {
                    $scope.recipe = response.data;
                    return response.data;
                })
                .then(function (recipe) {
                    if (recipe.fork_of_id) {
                        $recipeService.getRecipe(recipe.fork_of_id)
                            .then(function (response) {
                                $scope.recipe.fork_of = response.data;
                            });
                    }
                });

            function putComments () {
                $commentService.getCommentsForRecipe(recipeId)
                    .then(function (response) {
                        $scope.comments = response.data;
                    });
            }

            $scope.makeComment = function () {
                var self = this;
                $commentService.makeComment(recipeId, this.newComment)
                    .then(function() {
                        putComments();
                        self.newComment = '';
                    });
            };

            $scope.fork = function () {
                $recipeService.forkRecipe($scope.recipe.id)
                    .then(function (response) {
                        var newRecipeId = response.data.id;
                        $scope.go('/recipe/' + newRecipeId, {fork: 1});
                    });
            };

            putComments();

            function forkAlert() {
                $mdDialog.show(
                    $mdDialog.alert()
                        .clickOutsideToClose(true)
                        .title('This is your fork')
                        .ariaLabel('Fork')
                        .ok('Got it!')
                        .openFrom({
                            top: -50,
                            width: 30,
                            height: 80
                        })
                );
            }
        }]);

})();

