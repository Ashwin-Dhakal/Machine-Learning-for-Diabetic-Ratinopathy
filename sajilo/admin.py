from django.contrib import admin
from .models import All_hostel


class All_hostelModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'location','owner', 'email')
    class Meta:
        model = All_hostel


admin.site.register(All_hostel, All_hostelModelAdmin)

