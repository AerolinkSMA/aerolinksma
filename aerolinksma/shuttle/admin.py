import datetime

from django.contrib import admin

from aerolinksma.shuttle.models import Place, Client, Reservation


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_time', 'display_price', 'enabled')
    list_filter = ('enabled',)
    actions = ('make_enabled', 'make_disabled')

    def display_time(self, obj):
        """Display time readibly."""
        return '{} ({})'.format(datetime.timedelta(hours=obj.time),
                                obj.time)
    display_time.short_description = 'Time (h:m:s)'
    display_time.admin_order_field = 'time'

    def display_price(self, obj):
        """Display place's price with a leading dollar sign."""
        return '${}'.format(obj.price)
    display_price.short_description = 'Price'
    display_price.admin_order_field = 'price'

    def make_enabled(self, request, queryset):
        rows_updated = queryset.update(enabled=True)

        if rows_updated == 1:
            message_bit = '1 place was'
        else:
            message_bit = '{} places were'.format(rows_updated)
        self.message_user(request, '{} enabled'.format(message_bit))
    make_enabled.short_description = 'Enable selected places'
    make_enabled.allowed_permissions = ('change',)

    def make_disabled(self, request, queryset):
        rows_updated = queryset.update(enabled=False)

        if rows_updated == 1:
            message_bit = '1 place was'
        else:
            message_bit = '{} places were'.format(rows_updated)
        self.message_user(request, '{} disabled'.format(message_bit))
    make_disabled.short_description = 'Disable selected places'
    make_disabled.allowed_permissions = ('change',)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'place', 'direction', 'fare_type',
                    'paid', 'pickup_date', 'created_at')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email',
                    'phone_number')
