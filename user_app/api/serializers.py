from user_app.models import Account, Profile
from rest_framework import serializers

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True)
    password2 =serializers.CharField(write_only=True,required=True)
    old_password = serializers.CharField(write_only=True,required=True)
    class Meta:
        model=Account
        fields=('old_password','password','password2')
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Password not match"})
        return attrs
    def validate_old_password(self,value):
        user=self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password":"old password is incorrect"})
        return value
    def update(self,instance,validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ['password']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = Account
        fields = ['fullname',  'email', 'username', 'phone', 'password', 'password2']
        
        extra_kwargs = {
            'password':{'write_only':True}
        }
    
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        email = self.validated_data.get('email')
        phone = self.validated_data.get('phone')
        
        if password != password2 :
            raise serializers.ValidationError({'error':'Password should be the same'})
        if email:
            if Account.objects.filter(email=self.validated_data['email']).exists():
                raise serializers.ValidationError({'error':'Email id already exists'})
        elif phone:
            if Account.objects.filter(phone=self.validated_data['phone']).exists():
                raise serializers.ValidationError({'error':'phone already exists'})
        else:
            raise serializers.ValidationError({'error':'phone or email is required'})
        account = Account(
            fullname=self.validated_data['fullname'],
            username = self.validated_data['username'],
            email = self.validated_data.get('email'),
            phone = self.validated_data.get('phone')
            )
        account.set_password(password)
        account.save()

        return account

class AccountSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Account
        fields = ('email','phone','username','posts','comments')
        