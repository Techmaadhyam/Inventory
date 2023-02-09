from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
import barcode
from barcode.writer import ImageWriter
from .models import (
    PRODUCT_SERVICE,
    ITEM_UNIT,
    ITEM_TYPE,
    Category,
    Inventory,
    Warehouse,
    Rack
)
from .utils import generate_barcode
from django.contrib import messages


@method_decorator([login_required], name="dispatch")
class AddNewCategory(View):

    template_name: str = "add_new_category.html"
    def get(self, request):
        categories = Category.objects.filter(user=request.user).order_by('-updated_at')
        warehouse = Warehouse.objects.filter(user = request.user)
        return render(request, self.template_name, locals())

    def post(self, request):

        category = request.POST.get("category")        
        descriptions = request.POST.get("description")
        warehouse = request.POST['warehouse']
        print(warehouse)
        if category:
            if Category.objects.filter(user=request.user, name=category).exists():
                messages.error(request, 'Category Already Exists..!!!')

                return HttpResponseRedirect(reverse("add-category"), locals())
            else:
                warehouse = Warehouse.objects.get(id=warehouse)
                Category.objects.create(user=request.user, name=category, description = descriptions, warehouse = warehouse).save()
                messages.success(request, 'Category Added Successfully.')


        return redirect("add-category")


@method_decorator([login_required], name="dispatch")
class EditCategory(View):
    template_name: str = "update_category.html"
    def get(self, request, id):
        update_category = Category.objects.filter(user=request.user, id=id)
        return render(request, self.template_name, locals())

    def post(self, request, id):

        category = request.POST.get("category")        
        descriptions = request.POST.get("description")
        user_category = Category.objects.get(user=request.user, id=id)
        print('categgggggggobj',user_category)
        user_category.name = category
        user_category.description = descriptions
        user_category.save()

        return redirect("add-category")


@method_decorator([login_required], name="dispatch")
class DeleteCategory(View):

    def post(self, request, id):
        category = Category.objects.get(user=request.user, id=id)
        category.delete()
        return HttpResponseRedirect(reverse("add-category"))


@method_decorator([login_required], name="dispatch")
class AddInventoryItem(View):

    template_name: str = "inventory_dashboard.html"

    def get(self, request):
        # categories = Warehouse.objects.filter(user = request.user)
        categories = Category.objects.values('name').distinct().filter(user = request.user)
        # print(categories)
        racks = Rack.objects.values('rack').distinct().filter(user = request.user)
        search_id = request.GET.get("search_by_id")
        search_name = request.GET.get("search_by_name")
        search_category = request.GET.get("search_by_category")
        search_type = request.GET.get("search_by_type")
        search_hsn = request.GET.get("search_by_hsncode")
        units = ITEM_UNIT
        product_services = PRODUCT_SERVICE
        item_types = ITEM_TYPE
        warehouses = Warehouse.objects.filter(user = request.user)
        if search_id:
            items = Inventory.objects.filter(user=request.user, sku__icontains=search_id)
        elif search_name:
            items = Inventory.objects.filter(user=request.user, item_name__icontains=search_name).order_by('-updated_at')
        elif search_category:
            try:
                item_category = Category.objects.get(user=request.user, name__icontains=search_category)
                items = Inventory.objects.filter(user=request.user, item_category=item_category).order_by('-updated_at')
            except:
                items = Inventory.objects.filter(user=request.user).order_by('-updated_at')
        elif search_type:
            items = Inventory.objects.filter(user=request.user, type__icontains=search_type).order_by('-updated_at')
        elif search_hsn:
            items = Inventory.objects.filter(user=request.user, hsn_code__icontains=search_hsn).order_by('-updated_at')
        else:       
            items = Inventory.objects.filter(user=request.user).order_by('-updated_at')
        rack = Rack.objects.filter(user = request.user)
        return render(request, self.template_name, locals())

    def post(self, request):
        user = request.user
        item_sku = request.POST.get("item_sku")
        if Inventory.objects.filter(sku=item_sku).exists():
            messages.error(request, 'SKU item already exists..!!!')
            return HttpResponseRedirect(reverse("add-single-inventory-item"), locals())
        else:
            item_name = request.POST.get("item_name")
            stock = request.POST.get("stock")
            product_service = request.POST.get("service_product")
            unit = request.POST.get("unit")
            hsn_code = request.POST.get("hsn_code")
            type = request.POST.get("item_type")
            tax = request.POST.get("tax")
            price = request.POST.get("item_price")
            ware_house =  request.POST['category_load']
            print(ware_house)
            category = request.POST.get("category")
            rack = request.POST.get("add-racks")
  

            # print(request.POST)
            warehouse = Warehouse.objects.get(name=ware_house)
            item_category = Category.objects.get(id=category)
            items_rack = Rack.objects.get(id = rack)
            # print(request.POST)


            Inventory(user=request.user, price=price , item_rack = items_rack , item_name=item_name, sku=item_sku, stock=stock, product_or_service = product_service, unit_of_measurement = unit, hsn_code = hsn_code, type = type, tax = tax, warehouse = warehouse, item_category = item_category).save() # item_category=user_category,
            messages.success(request,'Inventory Added Successfully.')
            # Category(user = user, name = category_name).save()
            # Rack(rack = rack_name).save()
            # categories = Category.objects.filter(user = request.user)


        return HttpResponseRedirect(reverse("add-single-inventory-item"), locals())


# def warehouse(request):
    # categories = Warehouse.objects.filter(user = request.user)

    # if request.method == 'POST':
    #     print(request.POST)
    #     user = request.user
    #     warehouse_name = request.POST['warehouse_name']
    #     address = request.POST['address']
    #     description = request.POST['description']
    #     categories = request.POST['categories']
    #     # print(categories)
    #     new_category_name = request.POST.get('new_category_name')
    #     # print(new_category_name)
    #     rack = request.POST['racks']
    #     new_rack_name = request.POST.get('rack')
    #     box_number = request.POST['box_number']

    #     # print(warehouse)
    #     # warehouse.save()
       

    #     if categories == "Other":
    #         warehouse_category = Category(user = user, name = new_category_name)
    #         # print(category)
    #         # print("hello world")

    #     else:
    #         # print('hello')
    #         warehouse_category = Category(user = user, name = categories)

    #     if rack == "Other":
    #         warehouse_rack = Rack(user = user, rack = new_rack_name)
    #         # print("hello world")

    #     else:
    #         # print('hello')
    #         warehouse_rack = Rack(user = user, rack = rack)

    #     warehouse_rack.save()
    #     warehouse_category.save()
    #     warehouse = Warehouse(user = user, category = warehouse_category, rack =  warehouse_rack, name = warehouse_name, address = address, description = description, box_number = box_number)
    #     warehouse.save()
    #     # print(user, categories, warehouse_name, address)
        # if 'new_category_name' in request.POST:
        #     new_category_name = request.POST.get('new_category_name')
        #     Category(name = new_category_name).save()

        # if Category.objects.filter(name=categories).exists():
        #     category = Category(user = user, name = new_category_name, box_number = box_number)
        #     print(category)
        #     # category.save()

        # else:
        #     category = Category(user = user, name = categories, box_number = box_number)
        #     print('hello')
        #     print(category)
        #     # category.save()
        


        # if Category.objects.filter(name=categories).exists():
        #     category = Category(user = user, warehouse = warehouse, rack = racks, box_number = box_number)
        #     category.save()
        # else:
        #     category = Category(user = user, warehouse = warehouse, name = new_category_name, rack = racks, box_number = box_number)
        #     category.save()

       
        # return redirect('add-single-inventory-item')

    # return render(request, 'inventory_dashboard.html')

@method_decorator([login_required], name="dispatch")
class EditInventoryItem(View):

    template_name: str = "edit_inventory_items.html"

    def get(self, request, id):
        categories = Category.objects.filter(user=request.user)
        item_detail = Inventory.objects.filter(id=id)
        warehouses = Warehouse.objects.filter(user = request.user)
        all_racks = Rack.objects.order_by('-updated_at').filter(user = request.user)
        return render(request, self.template_name, locals())
    
    def post(self, request, id):
        print(request.POST)
        item_sku = request.POST.get("item_sku")
        item_name = request.POST.get("item_name")
        stock = request.POST.get("stock")
        category = request.POST.get("category")
        user_category = Category.objects.get(id=category)
        product_service = request.POST.get("service_product")
        unit = request.POST.get("unit")
        price = request.POST.get("item_price")
        hsn_code = request.POST.get("hsn_code")
        type = request.POST.get("item_type")
        tax = request.POST.get("tax")
        rack = request.POST.get("rack")
        racks = Rack.objects.get(id = rack)
        # j = Inventory.objects.filter(item_category__id = id)
        # print(j)


        warehouse_name = request.POST['ware_house']
        warehouse = Warehouse.objects.get(id = warehouse_name)

        item = Inventory.objects.filter(id=id).update(user=request.user, price=price, item_name=item_name, item_category = user_category, sku=item_sku, stock=stock, product_or_service=product_service, unit_of_measurement=unit, hsn_code=hsn_code, type=type, tax=tax,item_rack = racks, warehouse = warehouse)

        return HttpResponseRedirect(reverse("add-single-inventory-item"))


@method_decorator([login_required], name="dispatch")
class DeleteInventoryItem(View):

    def post(self, request, id):
        item_detail = Inventory.objects.get(id=id)
        item_detail.delete()
        return HttpResponseRedirect(reverse("add-single-inventory-item"))


@method_decorator([login_required], name="dispatch")
class AddWarehouse(View):
    
    template_name: str = 'add_warehouse.html'

    def get(self, request):
        user = request.user
        warehouses = Warehouse.objects.filter(user = user)
        category = Category.objects.filter(user = user).order_by('-id')
        racks = Rack.objects.all()
        return render(request, self.template_name, locals())
    def post(self, request):
        print(request.POST)
        user = request.user
        warehosue_name  = request.POST.get("warehouse_name")
        warehouse_location = request.POST.get("warehouse_loc")
        racks = request.POST.getlist("warehouse_racks")
        country = request.POST['country']
        description = request.POST['description']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code']
        if Warehouse.objects.filter(name=warehosue_name).exists():
            messages.error(request, 'Warehouse Already Exists...!!!')
        else:
            warehouse_obj = Warehouse(user = user, name = warehosue_name, address = warehouse_location, country = country, description = description, city = city, state = state, zip_code = zip_code)
            warehouse_obj.save()
            messages.success(request, 'Warehouse Created Successfully.')
            for rack in racks:
                warehouse_obj.rack.add(rack)
                warehouse_obj.save()
        return HttpResponseRedirect(reverse("add-warehouse"))


@method_decorator([login_required], name="dispatch")
class EditWarehouse(View):
    template_name: str = 'edit_warehouse.html'

    def get(self, request, id):

        # i = Category.objects.get(id=id)
        # j = Warehouse.objects.get(id=id)
        # category = Category.objects.filter(user = request.user)
        # rack = Rack.objects.filter(user = request.user)
        warhouse = Warehouse.objects.get(id = id)
        get_inventory_data = Inventory.objects.filter(warehouse__id = id)
        return render(request, self.template_name, locals())
    
    def post(self, request, id):
        i = Warehouse.objects.get(id = id)
        print(i)
        print(request.POST)
        user = request.user
        # name = request.POST.get("warehouse")
        # address = request.POST.get("address")
        warehouse_name = request.POST['warehouse_name']
        address = request.POST['address']
        description = request.POST['description']
        country = request.POST['country']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code']
        # box_number = request.POST['box_number']
        i.name = warehouse_name
        i.address = address
        i.description = description
        i.country = country
        i.city = city
        i.state = state
        i.zip_code = zip_code
        i.save()
       
        # if address and name:
        #     warehouse = Warehouse.objects.get(id=id)
        #     warehouse.name = name
        #     warehouse.address = address
        #     warehouse.save()
        

        return HttpResponseRedirect(reverse("home"))


@method_decorator([login_required], name="dispatch")
class DeleteWarehouse(View):
    template_name: str = 'add_warehouse.html'

    def post(self, request, id):
        warehouse = Warehouse.objects.get(id=id)
        warehouse.delete()
        return HttpResponseRedirect(reverse("add-warehouse"))


@method_decorator([login_required], name="dispatch")
class AddRack(View):
    template_name: str = 'add_rack.html'
    def get(self, request):
        racks = Rack.objects.order_by('-updated_at')
        warehouses = Warehouse.objects.filter(user = request.user)
        return render(request, self.template_name, locals())

    def post(self, request):
        user = request.user
        rack = request.POST.get("racks")
        ware_id = request.POST.get("warehouse")
        description = request.POST['description']
        # warehouse = Warehouse.objects.get(id=ware_id)
        # Rack.objects.create(user = user, warehouse = warehouse, rack = rack, description = description).save()

        if rack:
            if Rack.objects.filter(user=request.user, rack=rack).exists():
                messages.error(request, 'Rack Already Exists..!!!')

                return HttpResponseRedirect(reverse("add-rack"), locals())
            else:
                warehouse = Warehouse.objects.get(id=ware_id)
                Rack.objects.create(user = user, warehouse = warehouse, rack = rack, description = description).save()
                messages.success(request, 'Rack Created Successfully')

        
        return HttpResponseRedirect(reverse("add-rack"))
# select count(warehouse),sum(price), warehouse from inventory groupby warehouse

@method_decorator([login_required], name="dispatch")
class DeleteRack(View):
    template_name: str = 'add_rack.html'

    def post(self, request, id):
        rack = Rack.objects.get(id=id)
        rack.delete()
        return HttpResponseRedirect(reverse("add-rack"))


@method_decorator([login_required], name="dispatch")
class EditRack(View):
    template_name: str = 'edit_rack.html'

    def get(self, request, id):
        rack_detail = Rack.objects.get(id=id)
        return render(request, self.template_name, locals())
    def post(self, request, id):
        warehouse = request.POST.get('warehouse')
        rackname = request.POST.get('rack')
        warehouse_obj = Warehouse.objects.get(name=warehouse)
        rack = Rack.objects.get(id=id)
        rack.rack = rackname
        rack.warehosue = warehouse_obj
        rack.save()
        
        return HttpResponseRedirect(reverse("add-rack"))

@method_decorator([login_required], name="dispatch")
class GetWarehouseRack(View):

    def get(self, request, name):
        warehouse_obj = Warehouse.objects.get(name=name)
        rack_detail = Rack.objects.filter(warehouse=warehouse_obj)
        racks = []
        for rack in rack_detail:
            racks.append(rack.rack)
        context = {
            "status": 200,
            "racks": list(racks),
        }
        return JsonResponse(context)

def load_category(request):
    category_load = request.GET.get('category_load')
    # print(category_load)
    category = Category.objects.filter(warehouse__name = category_load)
    return render(request, 'load_category.html',{'category':category})

def load_rack(request):
    category_load = request.GET.get('category_load')
    # print(category_load)
    rack = Rack.objects.filter(warehouse__name = category_load)
    return render(request, 'load_rack.html', {'rack':rack})
