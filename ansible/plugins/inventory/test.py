from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    NAME = "test"

    def verify_file(self, path):
        valid = False
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(("test.yaml", "test.yml")):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=True):

        super(InventoryModule, self).parse(inventory, loader, path, cache)

        self.inventory.add_host("localhost")
        self.inventory.set_variable("localhost", "ansible_host", "localhost")
