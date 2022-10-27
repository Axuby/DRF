

from rest_framework import serializers

from watchlist_app.models import Review, StreamPlatform, WatchList


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class WatchListSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # len_name = serializers.SerializerMethodField()
    # reviews = ReviewSerializer(many=True, read_only=True)
    watchlist = serializers.CharField(source="watchlist")

    class Meta:
        model = WatchList
        # fields = ["id", "name", "description", "is_active"]
        fields = "__all__"

    def get_len_name(self, object):

        return len(object.title)

        # object-level
    def validate(self, data):
        if data["title"] == data["storyline"]:
            raise serializers.ValidationError(
                "Name and description should be different")
        return data

    # field-level

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name too short!")
        else:
            return value


class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True, read_only=True, view_name="movie-detail")

    class Meta:
        model = StreamPlatform
        fields = "__all__"
        # ["name", "about", "website", "watchlist"]

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField()
#     is_active = serializers.BooleanField()

#     def create(self, validated_data):
        # user = self.context['request'].user
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get(
#             'description', instance.description)
#         instance.is_active = validated_data.get(
#             'is_active', instance.is_active)
#         instance.save()
#         return instance

#     # object-level
#     def validate(self, data):
#         if data["name"] == data["description"]:
#             raise serializers.ValidationError(
#                 "Name and description should be different")
#         return data
# def validate(self, attrs):
   #     if Movie.objects.filter(name=attrs["name"], description=attrs["description"]).exists():
        #         if attrs.get("name") == attrs.get("description"):
        #             raise serializers.ValidationError(
        #                 "Name and description should be different")
        #         return data

        #     # field-level

        #     def validate_name(self, value):
        #         if len(value) < 2:
        #             raise serializers.ValidationError("Name too short!")
        #         else:
        #             return value
