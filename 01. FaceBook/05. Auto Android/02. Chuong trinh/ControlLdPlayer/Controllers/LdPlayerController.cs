using ControlLdPlayer.Services;
using ControlLdPlayer.ViewModels;
using ControlLdPlayer.Views;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ControlLdPlayer.Controllers
{
    public class LdPlayerController
    {
        private LdPlayer form;
        private LdPlayerViewModel view;

        public LdPlayerController(LdPlayer _form)
        {
            form = _form;
            view = new LdPlayerViewModel(form);
        }
        public void Create()
        {
            view.ReadName();
            string nameLd = view.Name;
            string command = $"add --name \"{nameLd}\"";
            CmdService.RunLdConsole(command);
        }

        public void Run()
        {
            view.ReadName();
            string nameLd = view.Name;
            string command = $"launch --name \"{nameLd}\"";
            CmdService.RunLdConsole(command);
        }

        public void Quit()
        {
            view.ReadName();
            string nameLd = view.Name;
            string command = $"quit --name \"{nameLd}\"";
            CmdService.RunLdConsole(command);
        }

        public void QuitAll()
        {
            string command = $"quitall";
            CmdService.RunLdConsole(command);
        }

        public void PropertySetting()
        {
            view.ReadName();
            view.ReadPropertySetting();
            string command = $"modify --name {view.Name} --resolution {view.Resolution} --cpu {view.Cpu} --memory {view.Memory} --imei {view.Imei}";
            CmdService.RunLdConsole(command);
        }
    }
}
